from kspi.rpc.client import Connection



class Vessel:

    TYPE_TAG = 'ksp.Vessel'

    def __init__(self, conn: Connection, id: str):
        self._conn = conn
        self._id = id


    @property
    def name(self) -> str:
        return self._conn.rpc(lambda ctx: self.name)
    
    @name.setter
    def name(self, v):
        def set_name(ctx):
            self.vesselName = v

        self._conn.rpc(set_name)



def vessel_setup_client_side_pickling(conn: Connection):
    def pickleClientSide(obj):
        if isinstance(obj, Vessel):
            return (Vessel.TYPE_TAG, obj._id)
        else:
            return None
        
    def unpickleClientSide(pid):
        type_tag, id = pid
        if type_tag == Vessel.TYPE_TAG:
            return Vessel(conn, id)
        else:
            return None
        
    conn.pickling.register_pickler_unpickler(pickleClientSide, unpickleClientSide)


def vessel_setup_server_side_pickling(conn: Connection):
    vessel_type_tag = Vessel.TYPE_TAG

    def setup(ctx):
        import System

        def pickleServerSide(obj):
            if isinstance(obj, ctx.clr.Vessel):
                return (vessel_type_tag, obj.id.ToString())
            else:
                return None
        
        def unpickleServerSide(pid):
            type_tag, id = pid
            if type_tag == vessel_type_tag:
                return ctx.clr.FlightGlobals.FindVessel(System.Guid(id))
            else:
                return None
            
        ctx.pickling.register_pickler_unpickler(pickleServerSide, unpickleServerSide)

    conn.rpc(setup)
