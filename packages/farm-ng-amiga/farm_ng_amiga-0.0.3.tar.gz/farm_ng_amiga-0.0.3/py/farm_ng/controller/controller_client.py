# Copyright (c) farm-ng, inc.
#
# Licensed under the Amiga Development Kit License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/farm-ng/amiga-dev-kit/blob/main/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import logging
from dataclasses import dataclass

import grpc
from farm_ng.controller import controller_pb2
from farm_ng.controller import controller_pb2_grpc

logging.basicConfig(level=logging.DEBUG)


@dataclass
class ControllerClientConfig:
    """Controller client configuration.

    Attributes:
        port (int): the port to connect to the server.
        address (str): the address to connect to the server.
    """

    port: int  # the port of the server address
    address: str = "localhost"  # the address name of the server


class ControllerServiceState:
    """Controller service state."""

    def __init__(self, proto: controller_pb2.ControllerServiceState = None) -> None:
        self._proto = controller_pb2.ControllerServiceState.UNAVAILABLE
        if proto is not None:
            self._proto = proto

    @property
    def value(self) -> int:
        return self._proto

    @property
    def name(self) -> str:
        return controller_pb2.ControllerServiceState.DESCRIPTOR.values[self.value].name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: ({self.value}, {self.name})"


class ControllerClient:
    def __init__(self, config: ControllerClientConfig) -> None:
        self.config = config

        self.logger = logging.getLogger(self.__class__.__name__)

        # create a async connection with the server
        self.channel = grpc.aio.insecure_channel(self.server_address)
        self.stub = controller_pb2_grpc.ControllerServiceStub(self.channel)

        self._state = ControllerServiceState()

    @property
    def state(self) -> ControllerServiceState:
        return self._state

    @property
    def server_address(self) -> str:
        """Returns the composed address and port."""
        return f"{self.config.address}:{self.config.port}"

    async def poll_service_state(self) -> None:
        while True:
            try:
                self._state = await self.get_state()
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                self.logger.info("Got Cancelled Error")
                break

    async def get_state(self) -> ControllerServiceState:
        state: ControllerServiceState
        try:
            response: controller_pb2.GetServiceStateResult = await self.stub.getServiceState(
                controller_pb2.GetServiceStateRequest()
            )
            state = ControllerServiceState(response.state)
        except grpc.RpcError:
            state = ControllerServiceState()
        self.logger.debug("ControllerServiceStub: port -> %i state is: %s", self.config.port, state)
        return state

    async def connect_to_service(self) -> None:
        state: ControllerServiceState = await self.get_state()
        if state.value == controller_pb2.ControllerServiceState.UNAVAILABLE:
            return
        await self.stub.startService(controller_pb2.StartServiceRequest())

    async def disconnect_from_service(self) -> None:
        state: controller_pb2.ControllerServiceState = await self.get_state()
        if state.value == controller_pb2.ControllerServiceState.UNAVAILABLE:
            return
        await self.stub.stopService(controller_pb2.StopServiceRequest())
