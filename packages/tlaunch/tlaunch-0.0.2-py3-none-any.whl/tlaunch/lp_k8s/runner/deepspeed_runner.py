#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
from tlaunch.lp_k8s.runner.script_runner import ScriptRunner
from tlaunch.lp_k8s.util import get_ipv4_by_hostname



class DeepSpeedRunner(ScriptRunner):
    def __init__(self, cmd, cmd_args, pwd):
        super().__init__(cmd, cmd_args, pwd)
        pass



