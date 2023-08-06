#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import launchpad as lp
import os
import sys
import uuid
import time
from argparse import REMAINDER, ArgumentParser
from tlaunch.lp_k8s.util import generate_tlaunchjob_name, get_namespace

def get_args_parser() -> ArgumentParser:
    """Helper function parsing the command line options."""

    parser = ArgumentParser(description="TLaunch Distributed Training Launcher")
    parser.add_argument("--lpjob_name", default=generate_tlaunchjob_name(), type=str, help="The name of this job")
    parser.add_argument("--namespace", default=get_namespace(), type=str, help="The namespace of this job")
    parser.add_argument("--image", default='docker.4pd.io/tlaunch/reverb:base', type=str, help="The docker image \
            of trainer")
    parser.add_argument("--image_pull_policy", choices=['Always','IfNotPresent','Never'], default="Always", type=str,
            help="The pull policy of image")
    parser.add_argument("--gpu", default=2, type=int, help="The number of gpu per trainer")
    parser.add_argument("--gpu_memory", default=3000, type=int, help="The memory size of each gpu")
    parser.add_argument("--gpu_cores", default=30, type=int, help="The maximum available cores of each gpu")
    parser.add_argument("--set_save_path", action='store_true', default=False, help="Whether to automatically set a \
            path to save the model, if use this option, TLaunch will generate a folder in TData/model and add a argument \
            --save_path for all trainer pods, which is pointing to this folder")
    parser.add_argument("--set_checkpoint_path", action='store_true', default=False, help="Whether to automatically set a \
            path to save the checkpoint file, if use this option, TLaunch will generate a file named last.tar.gz in \
            TData/model and add a argument --checkpoint_path for all trainer pods, which is pointing to this file. \
            This parameter is usually used to store checkpoint and elastic deployment")
    subparsers = parser.add_subparsers()

    # basic launcher
    parser_basic = subparsers.add_parser('basic')
    parser_basic.add_argument("--num_trainer", default=1, type=int, help="The number of trainer")
    parser_basic.add_argument("--set_share_file", action='store_true', default=False, help="Whether to automatically set \
            a cache file for transferring distributed shared information, if use this option, TLaunch will generate \
                pointing to this file")
    parser_basic.set_defaults(func=k8s_launch)
    parser_basic.add_argument("training_script_args", nargs=REMAINDER)

    # torchrun launcher
    parser_torchrun = subparsers.add_parser('torchrun')
    parser_torchrun.add_argument("--nnodes", default='1', type=str)
    parser_torchrun.add_argument("--nproc_per_node", default=1, type=int)
    parser_torchrun.add_argument("--rdzv_id", default=1, type=int)
    parser_torchrun.add_argument("--rdzv_backend", default="c10d", type=str)
    parser_torchrun.set_defaults(func=k8s_torchrun_launch)
    parser_torchrun.add_argument("training_script_args", nargs=REMAINDER)

    # deepspeed launcher
    parser_deepspeed = subparsers.add_parser('deepspeed')
    parser_deepspeed.add_argument("--num_nodes", default='1', type=str)
    parser_deepspeed.add_argument("--num_gpus", default='1', type=int)
    parser_deepspeed.set_defaults(func=k8s_deepspeed_launch)
    parser_deepspeed.add_argument("training_script_args", nargs=REMAINDER)
    return parser


def parse_args(args):
    parser = get_args_parser()
    return parser.parse_args(args)

def set_base_args(args, cmd_args):
    from tlaunch import lp_k8s
    save_path = os.path.join(lp_k8s.config.DEFAULT_MNT_PATH, 'models', args.lpjob_name)
    checkpoint_path = os.path.join(save_path, 'last.tar.gz')
    if args.set_save_path:
        cmd_args.extend(['--save_path', save_path])
        if os.path.exists(save_path) is not True:
            os.mkdir(save_path)
    if args.set_checkpoint_path:
        if os.path.exists(save_path) is not True:
            os.mkdir(save_path)
        cmd_args.extend(['--checkpoint_path', checkpoint_path])

def k8s_deepspeed_launch(args):
    from tlaunch.lp_k8s.runner.deepspeed_runner import DeepSpeedRunner
    from tlaunch import lp_k8s
    from tlaunch.lp_k8s import Config, Container, Resource

    cmd = 'deepspeed'
    cmd_args = [f'--num_nodes={args.nnodes}',
                f'--num_gpus={args.gpu}'] + args.training_script_args
    pwd = os.getcwd()

    set_base_args(args, cmd_args)
    program = lp.Program(args.lpjob_name)
    configs = {}
    namespace = args.namespace
    node_cmd_args = cmd_args
    node = lp_k8s.CourierNode(DeepSpeedRunner,
                              cmd=cmd,
                              cmd_args=node_cmd_args,
                              pwd=pwd)
    program.add_node(node, label='trainer')
    configs['trainer'] = Config(namespace=namespace,
                                container=Container(namespace=namespace,
                                                    resources=Resource(nvidia_gpu=args.gpu,
                                                                       nvidia_gpu_memory=args.gpu_memory,
                                                                       nvidia_gpu_cores=args.gpu_cores),
                                                    image=args.image,
                                                    image_pull_policy=args.image_pull_policy))

    lp_k8s.launch(program, namespace=namespace, group_config=configs)


def k8s_torchrun_launch(args):
    from tlaunch.lp_k8s.runner.torch_runner import TorchRunner
    from tlaunch import lp_k8s
    from tlaunch.lp_k8s import Config, Container, Resource
    from tlaunch.lp_k8s.util import get_hostname_by_lpjob

    cmd = 'torchrun'
    cmd_args = ['--nnodes={}'.format(args.nnodes),
                '--nproc_per_node={}'.format(args.nproc_per_node),
                '--rdzv_id={}'.format(args.rdzv_id),
                '--rdzv_backend={}'.format(args.rdzv_backend)] + args.training_script_args
    pwd = os.getcwd()

    set_base_args(args, cmd_args)
    rdzv_endpoint = get_hostname_by_lpjob(args.lpjob_name, 'trainer', 0)

    program = lp.Program(args.lpjob_name)
    configs = {}
    namespace = args.namespace
    num_trainer = int(args.nnodes.split(':')[-1])
    for rank in range(num_trainer):
        node_cmd_args = cmd_args
        node = lp_k8s.CourierNode(TorchRunner,
                                  rdzv_endpoint=rdzv_endpoint,
                                  cmd=cmd,
                                  cmd_args=node_cmd_args,
                                  pwd=pwd)
        program.add_node(node, label='trainer')
    configs['trainer'] = Config(namespace=namespace,
                                container=Container(namespace=namespace,
                                                    resources=Resource(nvidia_gpu=args.gpu,
                                                                       nvidia_gpu_memory=args.gpu_memory,
                                                                       nvidia_gpu_cores=args.gpu_cores),
                                                    image=args.image,
                                                    image_pull_policy=args.image_pull_policy,
                                                    ports=[('torch', 8002)]))

    lp_k8s.launch(program, namespace=namespace, group_config=configs)


def k8s_launch(args):
    from tlaunch.lp_k8s.runner.script_runner import ScriptRunner
    from tlaunch import lp_k8s
    from tlaunch.lp_k8s import Config, Container, Resource

    cmd = os.getenv("PYTHON_EXEC", sys.executable)
    cmd_args = ["-u"] + args.training_script_args + \
               ['--world_size', args.num_trainer]
    pwd = os.getcwd()
    set_base_args(args, cmd_args)
    if args.set_share_file:
        share_file = os.path.join(lp_k8s.config.DEFAULT_MNT_PATH, 'cache', args.lpjob_name, str(uuid.uuid4()))
        cmd_args.extend(['--share_file', share_file])

    program = lp.Program(args.lpjob_name)
    configs = {}
    namespace = args.namespace
    for rank in range(args.num_trainer):
        node_cmd_args = cmd_args.copy()
        node_cmd_args.extend(['--rank', rank])
        node = lp_k8s.CourierNode(ScriptRunner,
                                  cmd=cmd,
                                  cmd_args=node_cmd_args,
                                  pwd=pwd)
        program.add_node(node, label='trainer')
        configs['trainer'] = Config(namespace=namespace,
                                    container=Container(namespace=namespace,
                                                        resources=Resource(nvidia_gpu=args.gpu,
                                                                           nvidia_gpu_memory=args.gpu_memory,
                                                                           nvidia_gpu_cores=args.gpu_cores),
                                                        image=args.image,
                                                        image_pull_policy=args.image_pull_policy))

    lp_k8s.launch(program, namespace=namespace, group_config=configs)


def main():
    args = parse_args(sys.argv[1:])
    args.func(args)
