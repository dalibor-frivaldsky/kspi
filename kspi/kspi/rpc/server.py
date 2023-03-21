import clr
import rpyc
import threading

import System

from collections import namedtuple
from kspi.rpc.pickling import Pickling
from overrides import override
from rpyc.utils.server import ThreadedServer
from typing import Any, Callable



class ContextBuilder:

    def __init__(self):
        self._builders = []


    def register_builder(self, name, context_builder_fn: Callable[[], Any]):
        self._builders.append((name, context_builder_fn))


    def unregister_all(self):
        self._builders = []


    def build(self):
        ctx = namedtuple('ctx', " ".join([b[0] for b in self._builders]))(*[b[1]() for b in self._builders])

        return ctx



@rpyc.service
class KspiRpcService(rpyc.Service):

    @override
    def on_connect(self, conn: rpyc.Connection):
        import UnityEngine
        UnityEngine.Debug.Log('[KSPI] new connection: ' + str(conn))
        
        self._kspi_contex_builder = ContextBuilder()
        self._kspi_contex_builder.register_builder('ctx_builder', lambda: self._kspi_contex_builder)

        self._kspi_contex_builder.register_builder('conn', lambda: conn)

        self._kspi_pickling = Pickling()
        self._kspi_contex_builder.register_builder('pickling', lambda: self._kspi_pickling)


    @override
    def on_disconnect(self, conn: rpyc.Connection):
        import UnityEngine
        UnityEngine.Debug.Log('[KSPI] disconnection: ' + str(conn))


    @rpyc.exposed
    def rpc(self, fn_pickle):
        ctx = self._kspi_contex_builder.build()
        fn = self._kspi_pickling.loads(fn_pickle)
        result = [None]

        def call_fn_and_collect_result(fn, result):
            result[0] = fn(ctx)
        
        action = System.Action(lambda: call_fn_and_collect_result(fn, result))
        clr.UnityMainThreadDispatcher.Instance().EnqueueAsync(action).Wait()

        return self._kspi_pickling.dumps(result[0])
    


class Server:

    SERVER_PORT = 18811

    server = None
    serverThread = None


    @classmethod
    def run(cls):
        import UnityEngine

        cls.server = ThreadedServer(KspiRpcService, port=cls.SERVER_PORT)

        def start_server(server):
            server.start()
        
        cls.serverThread = threading.Thread(target=start_server, args=(cls.server,))
        cls.serverThread.start()

        UnityEngine.Debug.Log('[KSPI] RPC server running')


    @classmethod
    def stop_and_join_server_thread(cls):
        cls.server.close()
        cls.serverThread.join()