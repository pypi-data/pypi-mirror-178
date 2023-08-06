#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import logging


class ScriptRunner:
    def __init__(self, cmd, cmd_args, pwd, log=None):
        self.cmd = cmd
        self.cmd_args = cmd_args
        self.pwd = pwd
        self.log = log if log else logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        pass

    def run(self):
        self.log.info(f'Change path to {self.pwd}')
        os.chdir(self.pwd)
        cmd_str = self.cmd
        for arg in self.cmd_args:
            cmd_str += ' ' + str(arg)
        self.log.info(f'Run cmd: {cmd_str}')
        os.system(cmd_str)


