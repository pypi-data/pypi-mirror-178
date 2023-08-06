#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
from tlaunch.lp_k8s.runner.script_runner import ScriptRunner
from tlaunch.lp_k8s.util import get_ipv4_by_hostname
import logging


class TorchRunner(ScriptRunner):
    def __init__(self, rdzv_endpoint, cmd, cmd_args, pwd):
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        rdzv_endpoint = get_ipv4_by_hostname(rdzv_endpoint, log)[0] + ':8002'
        cmd_args = [f'--rdzv_endpoint={rdzv_endpoint}'] + cmd_args
        super().__init__(cmd, cmd_args, pwd, log)
        pass



