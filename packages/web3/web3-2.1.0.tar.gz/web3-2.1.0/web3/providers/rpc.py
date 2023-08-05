import contextlib
import gevent
from geventhttpclient import HTTPClient


from .base import BaseProvider  # noqa: E402


class RPCProvider(BaseProvider):
    def __init__(self, host="127.0.0.1", port="8545", *args, **kwargs):
        self.host = host
        self.port = port

        super(RPCProvider, self).__init__(*args, **kwargs)

    def make_request(self, method, params):
        from web3 import __version__ as web3_version
        request_data = self.encode_rpc_request(method, params)
        request_user_agent = 'Web3.py/{version}/{class_name}'.format(
            version=web3_version,
            class_name=type(self),
        )
        client = HTTPClient(
            host=self.host,
            port=self.port,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': request_user_agent,
            },
        )
        with contextlib.closing(client):
            response = client.post('/', body=request_data)
            response_body = response.read()

        return response_body


def is_testrpc_available():
    try:
        import testrpc  # noqa: F401
        return True
    except ImportError:
        return False


class TestRPCProvider(RPCProvider):
    def __init__(self, host="127.0.0.1", port=8545, *args, **kwargs):
        if not is_testrpc_available():
            raise Exception("`TestRPCProvider` requires the `eth-testrpc` package to be installed")
        from gevent.pywsgi import WSGIServer
        from testrpc.server import application
        from testrpc.testrpc import evm_reset

        evm_reset()

        self.server = WSGIServer(
            (host, port),
            application,
        )

        self.thread = gevent.spawn(self.server.serve_forever)

        super(TestRPCProvider, self).__init__(host, str(port), *args, **kwargs)
