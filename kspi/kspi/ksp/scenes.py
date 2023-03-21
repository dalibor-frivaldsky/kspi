from kspi.ksp.vessel import Vessel
from kspi.rpc.client import Connection



class FlightScene:

    def __init__(self, conn: Connection):
        self._conn = conn


    @property
    def active_vessel(self) -> Vessel:
        return self._conn.rpc(lambda ctx: ctx.clr.FlightGlobals.ActiveVessel)