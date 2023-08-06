import socket
import os
import time
from typing import Callable, Iterable, Iterator, Optional, TypeVar


T = TypeVar('T')
U = TypeVar('U')


def map_opt(opt: Optional[T], fn: Callable[[T], U]) -> Optional[U]:
  return None if opt is None else fn(opt)

def get_hostname_by_lpjob(lpjob_name: str, node_name: str, id: int) -> str:
    return f'{lpjob_name}-{node_name}-{id}.{lpjob_name}'

def get_ipv4_by_hostname(hostname, log = None):
    ip_list =  list(i[4][0] for i in socket.getaddrinfo(hostname, 0)
        if i[0] is socket.AddressFamily.AF_INET and i[1] is socket.SocketKind.SOCK_RAW)

    if len(ip_list) == 0:
        if log:
            log.info('WARNING: {} not found'.format(hostname))
        return get_ipv4_by_hostname(hostname, log)

    return ip_list

def get_namespace() -> str:
    if 'TPOD_NAMESPACE' in os.environ:
        namespace = os.environ['TPOD_NAMESPACE']
    else:
        namespace = 'default'
    return namespace

def generate_tlaunchjob_name():
    return "tlaunchjob-"+str(time.strftime("%H:%M:%S", time.localtime()))
