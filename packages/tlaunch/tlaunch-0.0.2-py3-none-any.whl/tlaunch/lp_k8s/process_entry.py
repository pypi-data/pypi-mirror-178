"""
Entry of a PythonNode worker.
This is mostly copied from launchpad, but slimmer.
Note that this is only usable with my implementation of lp-operator.
"""

import builtins
import contextlib
import logging
import os
import sys
import platform

from types import ModuleType

import cloudpickle


class DummyModule(ModuleType):
  def __getattr__(self, key):
    return None

  __all__ = []


# def tryimport(name, globals={}, locals={}, fromlist=[], level=0):
#   try:
#     return realimport(name, globals, locals, fromlist, level)
#   except ImportError:
#     print(f'Possibly missing import "{name}"')
#     return DummyModule(name)
#
#
# realimport, builtins.__import__ = builtins.__import__, tryimport

CONFIG_DIR = '/TData/cache'
SOURCE_DIR = '/workdir'
CODE_DIR = '/TData/code'

def main():
  # Allow for importing modules from the current directory.
  node_name, _, lp_task_id = platform.node().rpartition('-')
  job_name, _, node_name = node_name.rpartition('-')
  CACHE_DIR = os.path.join(CONFIG_DIR, job_name)
  task_id = int(lp_task_id)
  # os.system(f'bash {CODE_DIR}/setup.sh')
  if os.path.exists(SOURCE_DIR):
    for dirpath in os.listdir(SOURCE_DIR):
      path = os.path.join(SOURCE_DIR, dirpath)
      if os.path.islink(path):
        sys.path.append(path)

  functions = cloudpickle.load(open(os.path.join(CACHE_DIR, node_name), 'rb'))

  with contextlib.suppress():  # no-op context manager
    functions[task_id]()


if __name__ == '__main__':
  main()
