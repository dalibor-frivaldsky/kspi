from types import NoneType
from typing import Any, Union
from kspi.ksp.game import Game
from kspi.ksp.scenes import FlightScene
from kspi.ksp.spacecenter import SpaceCenter
from kspi.ksp.system import System
from kspi.rpc.client import Connection



class KSP:

    def __init__(self, conn: Connection):
        self._conn = conn

        self._game = Game(conn)
        self._space_center = SpaceCenter(conn)
        self._system = System(conn)


    @property
    def connection(self) -> Connection:
        return self._conn
    

    @property
    def game(self) -> Game:
        return self._game
    

    @property
    def space_center(self) -> SpaceCenter:
        return self._space_center


    @property
    def system(self) -> System:
        return self._system
    

    @property
    def scene(self) -> Union[FlightScene, NoneType]:
        scene_name = self._conn.rpc(lambda ctx: ctx.clr.HighLogic.LoadedScene.ToString())
        if scene_name == 'FLIGHT':
            return FlightScene(self._conn)
        else:
            return None