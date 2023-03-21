import time
from kspi.ksp.ksp import KSP
import pytest

from kspi.ksp.spacecenter import SpaceCenter
from kspi.ksp.system import System



@pytest.mark.integration
def test_vessel_rename(blank_game, common_picklings):
    conn, = blank_game
    ksp = KSP(conn)
    system = System(conn)
    space_center = SpaceCenter(conn)

    space_center.launch_ship('VAB', 'simple_ship', system.launch_sites[0])
    ksp.scene.active_vessel.name = 'new name'

    time.sleep(1.0)

    assert conn.rpc(lambda ctx: ctx.clr.FlightGlobals.ActiveVessel.vesselName) == 'new name'