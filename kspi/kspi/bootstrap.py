import kspi.ksp.system
import kspi.ksp.vessel

from kspi.command import Command
from kspi.ksp import KSP
from kspi.rpc.client import Connection



def initialize(host: str, port: int) -> Connection:
    conn = Connection(host, port)

    def bootstrap(ctx):
        import clr

        ctx.ctx_builder.register_builder('clr', lambda: clr)

    conn.rpc(bootstrap)

    kspi.ksp.system.launch_site_setup_client_side_pickling(conn)
    kspi.ksp.system.launch_site_setup_server_side_pickling(conn)

    kspi.ksp.vessel.vessel_setup_client_side_pickling(conn)
    kspi.ksp.vessel.vessel_setup_server_side_pickling(conn)

    ksp = KSP(conn)
    cmd = Command(ksp)

    return [conn, ksp, cmd]