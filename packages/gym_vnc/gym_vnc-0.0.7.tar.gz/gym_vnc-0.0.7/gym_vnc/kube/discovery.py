import json
import logging
import pipes
import subprocess

class Error(Exception):
    pass

logger = logging.getLogger()

def pretty_command(command):
    return ' '.join(pipes.quote(c) for c in command)

def log_command(command, prefix=''):
    logger.info('%sExecuting: %s', prefix, pretty_command(command))

def check_call(command, *args, **kwargs):
    log_command(command)
    return subprocess.check_call(command, *args, **kwargs)

def popen(command, *args, **kwargs):
    log_command(command)
    return subprocess.Popen(command, *args, **kwargs)

def check_with_output(command, *args, **kwargs):
    log_command(command)
    proc = subprocess.Popen(command, *args, stdout=subprocess.PIPE, **kwargs)
    stdout, _ = proc.communicate()
    if proc.returncode != 0:
        raise Error('Command {} returned non-zero exit status {}'.format(command, proc.returncode))
    return stdout

def interpret_ready(pod):
    # status:
    # conditions:
    # - lastProbeTime: null
    #   lastTransitionTime: 2016-07-06T05:29:45Z
    #   message: 'containers with unready status: [xdummy xvnc vnc-atari]'
    #   reason: ContainersNotReady
    #   status: "False"
    #   type: Ready
    if 'conditions' not in pod['status']:
        return False

    ready = [c for c in pod['status']['conditions'] if c['type'] == 'Ready']
    if not ready:
        return False

    return ready[0]['status'] == 'True'

def interpret_ports(containers):
    # TODO: clean up hack
    try:
        recorder = containers['vnc-recorder']
    except KeyError:
        pass
    else:
        spec = recorder['ports'][0]
        assert spec['containerPort'] == 5899
        return spec['hostPort'], None

    vnc_port_spec = containers['xvnc']['ports'][0]
    assert vnc_port_spec['containerPort'] == 5900
    vnc_port = vnc_port_spec['hostPort']

    app = [k for k in containers.keys() if k.startswith('vnc-')]
    assert len(app) == 1
    app = app[0]

    rewarder_port_spec = containers[app]['ports'][0]
    assert rewarder_port_spec['containerPort'] == 15900
    rewarder_port = rewarder_port_spec['hostPort']
    return vnc_port, rewarder_port

class VNCEnvDiscovery(object):
    def __init__(self):
        self.context = 'sci'
        self.namespace = 'gym'
        self.kubectl = ['kubectl', '--context', self.context, '--namespace', self.namespace]

    def discover_batches(self):
        pods = check_with_output(self.kubectl + ['get', 'pods', '-o', 'json', '-l', 'type=gym_vnc'])
        pods = json.loads(pods)

        batches = {}
        for pod in pods['items']:
            if 'deletionTimestamp' in pod['metadata']:
                # Pod has been deleted!
                continue

            batch = pod['metadata']['labels']['batch']
            if batch not in batches:
                batches[batch] = {'count': 0}
            batches[batch]['count'] += 1
        return batches

    def discover(self, batch, force_ready=False):
        pods = check_with_output(self.kubectl + ['get', 'pods', '-o', 'json', '-l', 'type=gym_vnc', '-l', 'batch={}'.format(batch)])
        pods = json.loads(pods)

        if len(pods['items']) == 0:
            raise Error('Incorrect batch id: {}'.format(batch))

        remotes = []

        for pod in pods['items']:
            name = pod['metadata']['name']
            containers = {}
            for container in pod['spec']['containers']:
                containers[container['name']] = container
            vnc_port, rewarder_port = interpret_ports(containers)
            node = pod['spec'].get('nodeName')

            # Not scheduled on a node yet
            if node is None:
                if force_ready:
                    raise Error('Not all pods ready: {} is not scheduled on a node yet'.format(name))
                continue

            spec = {
                'name': name,
                'vnc_address': '{}:{}'.format(node, vnc_port),
                'ready': interpret_ready(pod),
            }
            if rewarder_port:
                # Not true for VNC recorder
                spec['rewarder_address'] = '{}:{}'.format(node, rewarder_port)
            remotes.append(spec)
        return remotes

vnc_env_discovery = VNCEnvDiscovery()
discover = vnc_env_discovery.discover
discover_batches = vnc_env_discovery.discover_batches
