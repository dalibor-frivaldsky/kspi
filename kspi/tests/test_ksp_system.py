import pytest

from kspi.ksp.game import Game
from kspi.ksp.system import System, LaunchSite, launch_site_setup_client_side_pickling, launch_site_setup_server_side_pickling



@pytest.mark.integration
def test_system_get_launch_sites(blank_game):
    conn, = blank_game
    launch_site_setup_client_side_pickling(conn)
    launch_site_setup_server_side_pickling(conn)

    launch_sites = System(conn).launch_sites

    assert len(launch_sites) > 0
    assert isinstance(launch_sites[0], LaunchSite) == True