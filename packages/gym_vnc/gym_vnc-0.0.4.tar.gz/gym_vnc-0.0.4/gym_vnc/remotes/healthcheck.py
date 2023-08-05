import errno
import logging
import select
import socket
import time

from gym_vnc import error
from gym.utils import reraise

logger = logging.getLogger(__name__)

def run(vnc_addresses, rewarder_addresses, timeout=None, start_timeout=None):
    healthcheck = Healthcheck(vnc_addresses, rewarder_addresses, timeout=timeout, start_timeout=start_timeout)
    healthcheck.run()

def host_port(address, default_port=None):
    split = address.split(':')
    if len(split) == 1:
        host = split[0]
        port = default_port
    else:
        host, port = split
        port = int(port)
    return host, port

class Healthcheck(object):
    def __init__(self, vnc_addresses, rewarder_addresses, timeout=None, start_timeout=None):
        self.timeout = timeout or (4 * len(vnc_addresses) + 20)
        self.start_timeout = start_timeout

        start_time = time.time()

        self.sockets = {}
        for address in vnc_addresses:
            self._register_vnc(address, start_time)
        for address in rewarder_addresses:
            self._register_rewarder(address, start_time)

    def _register_vnc(self, address, start_time=None):
        if start_time is None:
            start_time = time.time()

        host, port = host_port(address, default_port=5900)

        while True:
            # In VNC, the server sends bytes upon connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((host, port))
            except socket.error as e:
                if self.start_timeout is None or socket.errno.ECONNREFUSED != e.errno:
                    reraise(suffix='while connecting to VNC server {}'.format(address))
                    logger.info('VNC server %s did not come up yet (error: %s). Sleeping for 1s.', address, e)
                time.sleep(1)
            else:
                break

            if time.time() - start_time > self.start_timeout:
                raise error.Error('VNC server {} did not come up within {}s'.format(address, self.start_timeout))

        self.sockets[sock] = ('vnc', address)

    def _register_rewarder(self, address, start_time=None):
        if start_time is None:
            start_time = time.time()

        host, port = host_port(address, default_port=15900)

        while True:
            # In WebSockets, the server sends bytes once we've upgraded the protocol
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((host, port))
            except socket.error as e:
                if self.start_timeout is None or socket.errno.ECONNREFUSED != e.errno:
                    reraise(suffix='while connecting to Rewarder server {}'.format(address))
                logger.info('Rewarder server %s did not come up yet (error: %s). Sleeping for 1s.', address, e)
                time.sleep(1)
            else:
                break

            if time.time() - start_time > self.start_timeout:
                raise error.Error('Rewarder server {} did not come up within {}s'.format(address, self.start_timeout))

        sock.send('GET / HTTP/1.1\r\nHost: 127.0.0.1:10003\r\nUpgrade: WebSocket\r\nConnection:Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n')
        self.sockets[sock] = ('rewarder', address)

    def run(self):
        target = time.time() + self.timeout
        while self.sockets:
            remaining = target - time.time()
            if remaining < 0:
                break
            ready, _, _ = select.select(self.sockets.keys(), [], [], remaining)

            # Go through the readable sockets
            remote_closed = False
            for sock in ready:
                type, address = self.sockets.pop(sock)

                # Connection was closed; try again.
                #
                # This is guaranteed not to block.
                try:
                    recv = sock.recv(1)
                except socket.error as e:
                    if e.errno == errno.ECONNRESET:
                        recv = ''
                    else:
                        raise

                if recv == '':
                    logger.info('Remote closed: address=%s', address)
                    remote_closed = True
                    if type == 'rewarder':
                        self._register_rewarder(address)
                    else:
                        self._register_vnc(address)

                sock.close()

            if remote_closed:
                sleep = 1
                logger.info('At least one sockets was closed by the remote. Sleeping %ds...', sleep)
                time.sleep(sleep)

        if self.sockets:
            raise error.Error('Not all servers came up within {}s: {}'.format(self.timeout, self.sockets.values()))
