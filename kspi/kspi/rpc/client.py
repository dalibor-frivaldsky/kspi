import rpyc

from kspi.rpc.pickling import Pickling



class Connection:
    
    def __init__(self, host: str, port: int):
        self.conn = rpyc.connect(host, port)
        self.pickling = Pickling()
        
        
    def close(self):
        self.conn.close()
        
        
    def rpc(self, fn: callable):
        fn_pickle = self.pickling.dumps(fn)
        
        return self.pickling.loads(self.conn.root.rpc(fn_pickle))