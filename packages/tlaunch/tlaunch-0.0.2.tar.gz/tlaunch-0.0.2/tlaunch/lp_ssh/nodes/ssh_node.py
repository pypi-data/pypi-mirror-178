#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2021 The TARTRL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""""""
import os
import json
from pathlib import Path

from typing import Any, List, Mapping, Optional, Union, Sequence, Tuple
import shutil

import atexit

import cloudpickle
import tempfile

from launchpad.nodes.python.local_multi_processing import PythonProcess, _to_cmd_arg, flags_utils
from tlaunch.lp_ssh import context

from tlaunch.lp_ssh.launch.ssh_multi_processing import commands as mp_commands

from .python.node import PyClassNode

_DATA_FILE_NAME = 'job.pkl'


def to_ssh_multiprocessing_executables(
        nodes: Sequence[Any], label: str, launch_config: PythonProcess,
        pdb_post_mortem: bool) -> List[mp_commands.Command]:
    """Returns a list of `Command`s objects for the given `PyNode`s."""

    launch_config = launch_config or PythonProcess()
    if not isinstance(launch_config, PythonProcess):
        raise ValueError(
            'Launch config for {} must be a PythonProcess.'.format(label))

    #
    # mannully set entry script path

    # 在分布式系统中，这个data_file有两种参考的实现形式，一种是通过共享文件的形式，所有机器能访问一个统一的文件路径
    # 第二个实现方式是通过打包文件，然后把整个文件发送到远程机器上，远程机器加在本地文件即可
    # 这里我们采用第一种，通过共享文件夹路径的形式来加载'process_entry.py'和'job.pkl'

    if nodes[0].share_entry_script_path:
        entry_script_path = nodes[0].share_entry_script_path
    else:
        entry_script_path = os.path.join(os.path.dirname(__file__), 'python',
                                         'process_entry.py')
    if nodes[0].share_temp_dir:
        if not Path(nodes[0].share_temp_dir).exists():
            os.makedirs(nodes[0].share_temp_dir)
        tmp_dir = tempfile.mkdtemp(dir=nodes[0].share_temp_dir)
    else:
        tmp_dir = tempfile.mkdtemp()

    # debug = True
    # if debug:
    #   # 这里为tlaunch分布式执行时，代码的入口，后面需要改成自动加载这个入口
    #   entry_script_path = '/home/shiyu/mfs/Task/TARTRL/github/tmarl/tmarl/tlaunch/lp_ssh/nodes/python/process_entry.py'
    #   tmp_dir = tempfile.mkdtemp(dir=os.path.join(os.getenv("HOME"), 'mfs/tmp/'))

    rm_tmp_dir = False
    if rm_tmp_dir:
        atexit.register(shutil.rmtree, tmp_dir, ignore_errors=True)


    data_file_path = os.path.join(tmp_dir, _DATA_FILE_NAME)
    with open(data_file_path, 'wb') as f:
        cloudpickle.dump([node.function for node in nodes], f,protocol=4)

    commands = []
    if hasattr(nodes[0], "host"):
        group_host = nodes[0].host
        group_port = nodes[0].port
    else:
        group_host = "localhost"
        group_port = "22"

    for task_id, node in enumerate(nodes):
        assert not hasattr(node, "host") or group_host == node.host, 'Nodes in the same group must have the same host. Node {} in group {} should run on host {} instead of {}'.format(
            task_id, label, group_host, node.host)
        command_as_list = [
            launch_config.absolute_interpreter_path, entry_script_path
        ]

        # Arguments to pass to the script
        for key, value in launch_config.args.items():
            command_as_list.extend(_to_cmd_arg(key, value))

        # Find flags and pre-populate their definitions, as these definitions are
        # not yet ready in the entry script.
        flags_to_populate = flags_utils.get_flags_to_populate(
            list(launch_config.args.items()))
        if flags_to_populate:
            command_as_list.extend(
                _to_cmd_arg('flags_to_populate', json.dumps(flags_to_populate)))

        command_as_list.extend([
            '--data_file', data_file_path,
            '--lp_task_id', str(task_id),
        ])
        command = mp_commands.Command(command_as_list, launch_config.env,
                                      label + '/' + str(task_id), group_host, group_port)

        commands.append(command)

    return commands


class SSHNode(PyClassNode):
    share_entry_script_path: str = None
    share_temp_dir: str = None

    def run(self) -> None:
        super().run()

    def to_host(self, host):
        if ":" in host:
            self.host = host.split(":")[0]
            self.port = host.split(":")[1]
        else:
            self.host = host
            self.port = "22"
        return self

    @staticmethod
    def to_executables(nodes, label, launch_context):
        return to_ssh_multiprocessing_executables(
            nodes, label, launch_context.launch_config, pdb_post_mortem=False)
