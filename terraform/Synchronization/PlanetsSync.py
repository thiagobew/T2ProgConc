from threading import Lock
from Config.Singleton import Singleton
import globals
from Enum.Enum import Polo


class PlanetsSync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__polesMutexDic = {}
            self.__polesMutexDic[Polo.NORTH] = {}
            self.__polesMutexDic[Polo.SOUTH] = {}
            planets = globals.get_planets_ref()
            for key in planets:
                self.__polesMutexDic[Polo.NORTH][key] = Lock()
                self.__polesMutexDic[Polo.SOUTH][key] = Lock()

    @property
    def polesMutexDic(self) -> Lock:
        return self.__polesMutexDic
