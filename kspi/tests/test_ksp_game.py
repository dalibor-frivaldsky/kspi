import pytest

from kspi.ksp.game import Game



@pytest.mark.integration
def test_ksp_game_load_game(ksp_connection, finish_in_main_menu):
    game = Game(ksp_connection)
    save_folder = 'integration_tests'
    file_name = 'blank'

    game.load(save_folder, file_name)

    game_title, scene, time_loaded = ksp_connection.rpc(lambda ctx: [
        ctx.clr.HighLogic.CurrentGame.Title,
        ctx.clr.HighLogic.LoadedScene.ToString(),
        ctx.clr.HighLogic.TimeSceneLoaded
    ])

    assert game_title == 'integration_tests (SANDBOX)'
    assert scene == 'SPACECENTER'
    assert time_loaded > 0