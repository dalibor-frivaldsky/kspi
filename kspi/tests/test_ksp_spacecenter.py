import pytest

from kspi.ksp.spacecenter import SpaceCenter
from kspi.ksp.system import System



@pytest.mark.integration
def test_space_center_launch_ship(blank_game, common_picklings):
    conn, = blank_game
    system = System(conn)
    space_center = SpaceCenter(conn)

    space_center.launch_ship('VAB', 'simple_ship', system.launch_sites[0])

    assert conn.rpc(lambda ctx: ctx.clr.HighLogic.LoadedScene.ToString()) == 'FLIGHT'
    assert conn.rpc(lambda ctx: ctx.clr.FlightGlobals.ActiveVessel) != None