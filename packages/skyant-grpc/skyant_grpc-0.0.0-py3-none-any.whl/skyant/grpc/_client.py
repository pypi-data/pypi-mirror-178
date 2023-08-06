'''
'''


class Client():
    '''
    '''

    def __init__(self, host: str = '127.0.0.1', port: int = 443):

        self._host = host
        self._port = port

    @property
    # pylint: disable=missing-docstring
    def url(self) -> str:
        return f'{self._host}:{self._port}'

    @property
    # pylint: disable=missing-docstring
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    # pylint: disable=missing-docstring
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port):
        self._port = port
