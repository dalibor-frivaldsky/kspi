from kspi.rpc.client import Connection



class Game:

    def __init__(self, conn: Connection):
        self._conn = conn


    def load(self, save_folder: str, file_name: str):
        def start_loaded_game(ctx):
            game = ctx.clr.GamePersistence.LoadGame(file_name, save_folder, True, True)
            ctx.clr.HighLogic.CurrentGame = game
            ctx.clr.HighLogic.CurrentGame.startScene = ctx.clr.GameScenes.SPACECENTER
            ctx.clr.HighLogic.SaveFolder = save_folder
            ctx.clr.HighLogic.CurrentGame.Start()

        self._conn.rpc(start_loaded_game)

        def restore_loaded_game_state(ctx):
            game = ctx.clr.GamePersistence.LoadGame(file_name, save_folder, True, True)
            game.Load()

        self._conn.rpc(restore_loaded_game_state)
