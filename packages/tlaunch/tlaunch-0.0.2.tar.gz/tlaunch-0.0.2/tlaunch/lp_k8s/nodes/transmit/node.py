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

from typing import Callable, Optional, Sequence
import launchpad as lp
import reverb

from ...node.reverb import ReverbNode, ReverbHandle
from ...node import common

PriorityTablesFactory = Callable[[], Sequence[reverb.Table]]
CheckpointerFactory = Callable[[], reverb.checkpointers.CheckpointerBase]

TRANSMIT_PORT_NAME = 'transmit'


class TransmitNode(ReverbNode):
    """Represents a Transmit Server in a Launchpad program."""

    def __init__(self, Client, Server, *args, **kwargs):
        self.Client = Client
        self.Server = Server
        super().__init__(*args, **kwargs)

    def run(self):
        priority_tables = self._priority_tables_fn()
        priority_tables.append(reverb.Table(name='info',
                                            sampler=reverb.selectors.Uniform(),
                                            remover=reverb.selectors.Fifo(),
                                            max_size=1,
                                            rate_limiter=reverb.rate_limiters.Queue(1),
                                            ))

        if self._checkpoint_ctor is None:
            checkpointer = None
        else:
            checkpointer = self._checkpoint_ctor()

        self._server = self.Server(
            tables=priority_tables,
            port=lp.get_port_from_address(
                self._address.resolve()),
            checkpointer=checkpointer)
        common.wait_for_stop()

    def create_handle(self):
        return self._track_handle(ReverbHandle(self._address, self.Client))