#!/usr/bin/env python

import argparse
import os
import subprocess
import sys
import threading
from collections import OrderedDict

import yaml
import yodl

debug = False


class DockerCompose:
    def __init__(self, compose, project, compose_base_dir, requested_services):
        self.project = project
        self.compose_base_dir = compose_base_dir
        self.services = self.merge_services(compose.get('services', {}))
        self.networks = compose.get('networks', {})
        self.volumes = compose.get('volumes', {})
        self.filtered_services = filter(lambda service: not requested_services or service in requested_services, self.services)

    def project_prefix(self, value):
        return '{}_{}'.format(self.project, value)

    def merge_services(self, services):
        result = OrderedDict()

        for service in services:
            service_config = services[service]
            result[service] = service_config

            if 'extends' in service_config:
                extended_config = service_config['extends']
                extended_service = extended_config['service']

                del result[service]['extends']

                if 'file' in extended_config:
                    extended_service_data = self.merge_services(
                        yaml.load(open(self.compose_base_dir + extended_config['file'], 'r'), yodl.OrderedDictYAMLLoader)['services']
                    )[extended_service]
                else:
                    extended_service_data = result[extended_service]

                for k, v in extended_service_data.items():
                    if k not in result[service]:
                        result[service][k] = v

        return result

    @staticmethod
    def call(cmd, ignore_return_code=False):
        print('Running: \n' + cmd + '\n')
        if not debug:
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            returncode = ps.wait()
            stdout = ps.communicate()[0]
            if returncode != 0 and not ignore_return_code:
                print >> sys.stderr, ('Error: command "{}" failed: {}'.format(cmd, stdout))
                sys.exit(returncode)
            else:
                return stdout

    def is_service_exists(self, service):
        return self.call('docker service ls -f name={} | tail -n +2'.format(self.project_prefix(service)))

    def is_external_network(self, network):
        return isinstance(self.networks[network], dict) and 'external' in self.networks[network]

    def up(self):
        for network in self.networks:
            if not self.is_external_network(network):
                cmd = '[ "`docker network ls -f name={0} | tail -n +2`" != "" ] || docker network create --driver overlay --opt encrypted {0}' \
                    .format(self.project_prefix(network))
                self.call(cmd)

        for volume in self.volumes:
            cmd = '[ "`docker volume ls -f name={0} | tail -n +2`" != "" ] || docker volume create --name {0}'.format(self.project_prefix(volume))
            self.call(cmd)

        services_to_start = []

        for service in self.filtered_services:
            if self.is_service_exists(service):
                services_to_start.append(service)
                continue

            service_config = self.services[service]
            cmd = ['docker service create --with-registry-auth \\\n --name', self.project_prefix(service), '\\\n']

            service_image = []
            service_command = []

            for parameter in service_config:
                value = service_config[parameter]

                def restart():
                    cmd.extend(['--restart-condition', {'always': 'any'}[value], '\\\n'])

                def logging():
                    cmd.extend(['--log-driver', value['driver'], '\\\n'])
                    log_opts = value['options']
                    for k, v in log_opts.items():
                        cmd.extend(['--log-opt', '{}={}'.format(k, v), '\\\n'])

                def mem_limit():
                    cmd.extend(['--limit-memory', value, '\\\n'])

                def image():
                    service_image.append(value)

                def command():
                    service_command.extend(value.split(' '))

                def expose():
                    pass  # unsupported

                def container_name():
                    pass  # unsupported

                def hostname():
                    pass  # unsupported; waiting for https://github.com/docker/docker/issues/24877

                def extra_hosts():
                    pass  # unsupported

                def ports():
                    for port in value:
                        cmd.extend(['--publish', port, '\\\n'])

                def networks():
                    for network in value:
                        cmd.extend(['--network', network if self.is_external_network(network) else self.project_prefix(network), '\\\n'])

                def volumes():
                    for volume in value:
                        src, dst = volume.split(':')

                        if src.startswith('.'):
                            src = src.replace('.', self.compose_base_dir, 1)

                        if src.startswith('/'):
                            cmd.extend(['--mount', 'type=bind,src={},dst={}'.format(src, dst), '\\\n'])
                        else:
                            cmd.extend(['--mount', 'src={},dst={}'.format(self.project_prefix(src), dst), '\\\n'])

                def environment():
                    if isinstance(value, dict):
                        for k, v in value.items():
                            cmd.extend(['--env', '{}={}'.format(k, v), '\\\n'])
                    else:
                        for env in value:
                            if env.startswith('constraint') or env.startswith('affinity'):
                                constraint = env.split(':', 2)[1]
                                cmd.extend(['--constraint', "'{}'".format(constraint), '\\\n'])
                            else:
                                cmd.extend(['--env', env, '\\\n'])

                def replicas():
                    cmd.extend(['--replicas', value, '\\\n'])

                def unsupported():
                    print('WARNING: unsupported parameter {}'.format(parameter))

                locals().get(parameter, unsupported)()

            cmd.extend(service_image)
            cmd.extend(service_command)

            self.call(' '.join(cmd))

        if services_to_start:
            self.start(services_to_start)

    def pull(self):
        nodes = self.call("docker node ls | grep Ready | awk -F'[[:space:]][[:space:]]+' '{print $2}'").rstrip().split('\n')

        threads = []

        for node in nodes:
            cmd = '; '.join(['docker -H tcp://{}:2375 pull {}'.format(node, self.services[service]['image']) for service in self.filtered_services])
            threads.append((node, threading.Thread(target=self.call, args=(cmd,))))

        for node, thread in threads:
            print('Pulling on node {}'.format(node))
            thread.start()

        for node, thread in threads:
            thread.join()
            print('Node {} - DONE'.format(node))

    def stop(self):
        services = filter(self.is_service_exists, self.filtered_services)
        cmd_args = ['{}={}'.format(self.project_prefix(service), 0) for service in services]
        if cmd_args:
            self.call('docker service scale ' + ' '.join(cmd_args))

    def rm(self):
        services = filter(self.is_service_exists, self.filtered_services)
        cmd_args = [self.project_prefix(service) for service in services]
        if cmd_args:
            self.call('docker service rm ' + ' '.join(cmd_args))

    def start(self, services=None):
        if services is None:
            services = self.filtered_services

        cmd = 'docker service scale ' + \
              ' '.join(['{}={}'.format(self.project_prefix(service), self.services[service].get('replicas', '1')) for service in services])
        self.call(cmd)


def main():
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=120))
    parser.add_argument('-f', '--file', type=argparse.FileType(), help='Specify an alternate compose file (default: docker-compose.yml)', default='docker-compose.yml')
    parser.add_argument('-p', '--project-name', help='Specify an alternate project name (default: directory name)')
    parser.add_argument('--dry-run', action='store_true')
    subparsers = parser.add_subparsers(title='Command')
    parser.add_argument('_service', metavar='service', nargs='*', help='List of services to run the command for')

    services_parser = argparse.ArgumentParser(add_help=False)
    services_parser.add_argument('service', nargs='*', help='List of services to run the command for')

    pull_parser = subparsers.add_parser('pull', help='Pull service images', add_help=False, parents=[services_parser])
    pull_parser.set_defaults(command='pull')

    rm_parser = subparsers.add_parser('rm', help='Stop and remove services', add_help=False, parents=[services_parser])
    rm_parser.set_defaults(command='rm')
    rm_parser.add_argument('-f', help='docker-compose compatibility; ignored', action='store_true')

    start_parser = subparsers.add_parser('start', help='Start services', add_help=False, parents=[services_parser])
    start_parser.set_defaults(command='start')

    stop_parser = subparsers.add_parser('stop', help='Stop services', add_help=False, parents=[services_parser])
    stop_parser.set_defaults(command='stop')

    up_parser = subparsers.add_parser('up', help='Create and start services', add_help=False, parents=[services_parser])
    up_parser.set_defaults(command='up')
    up_parser.add_argument('-d', help='docker-compose compatibility; ignored', action='store_true')

    args = parser.parse_args(sys.argv[1:])

    global debug
    debug = args.dry_run

    compose_base_dir = os.path.dirname(os.path.abspath(args.file.name))

    if not args.project_name:
        args.project_name = os.path.basename(compose_base_dir)

    docker_compose = DockerCompose(yaml.load(args.file, yodl.OrderedDictYAMLLoader), args.project_name, compose_base_dir + '/', args.service)
    getattr(docker_compose, args.command)()


if __name__ == "__main__":
    main()
