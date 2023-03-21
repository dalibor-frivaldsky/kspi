import pytest

from kspi.ksp.game import Game
from kspi.ksp.system import launch_site_setup_client_side_pickling, launch_site_setup_server_side_pickling
from kspi.ksp.vessel import vessel_setup_client_side_pickling, vessel_setup_server_side_pickling
from kspi.rpc.client import Connection



@pytest.fixture(scope='session')
def ksp_connection():
    host = 'localhost'
    port = 18811

    conn = Connection(host, port)

    def bootstrap(ctx):
        import clr

        ctx.ctx_builder.register_builder('clr', lambda: clr)

    conn.rpc(bootstrap)

    yield conn

    conn.close()



@pytest.fixture
def finish_in_main_menu(ksp_connection):
    yield

    ksp_connection.rpc(lambda ctx: ctx.clr.HighLogic.LoadScene(ctx.clr.GameScenes.MAINMENU))



@pytest.fixture
def blank_game(ksp_connection, finish_in_main_menu):
    Game(ksp_connection).load('integration_tests', 'blank')

    yield [ksp_connection]



@pytest.fixture
def common_picklings(ksp_connection):
    launch_site_setup_client_side_pickling(ksp_connection)
    launch_site_setup_server_side_pickling(ksp_connection)

    vessel_setup_client_side_pickling(ksp_connection)
    vessel_setup_server_side_pickling(ksp_connection)
