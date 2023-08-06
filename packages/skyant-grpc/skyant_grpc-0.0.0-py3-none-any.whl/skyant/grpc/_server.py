'''
'''

import asyncio
import grpc
from grpc_reflection.v1alpha import reflection


# pylint: disable=missing-docstring
def _assert_port(port: int) -> None:
    assert port > 0 and port < 65536, 'Port number must be between 1 and 65535'


class Server():
    '''
    '''

    def __init__(self, port: int = 8008):

        self._server = grpc.aio.server()
        _assert_port(port)
        self._port = port
        self._loop = asyncio.get_event_loop()

    # pylint: disable=missing-docstring
    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value: int):
        _assert_port(value)
        self._port = value

    def attach(self, skyapp_inf, worker_obj, service_name: str = None) -> None:
        '''
        '''

        service_mod = getattr(skyapp_inf, 'service')
        message_mod = getattr(skyapp_inf, 'message')
        service_name = service_name if service_name else worker_obj.__name__

        attacher = getattr(service_mod, f'add_{service_name}Servicer_to_server')
        attacher(worker_obj(), self._server)
        reflector = (
            message_mod.DESCRIPTOR.services_by_name[service_name].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(reflector, self._server)

    # pylint: disable=missing-docstring
    async def _insecure(self):

        self._server.add_insecure_port(f'[::]:{self._port}')
        await self._server.start()
        await self._server.wait_for_termination()

    def insecure(self):
        '''
        '''

        self._loop.run_until_complete(self._insecure())
