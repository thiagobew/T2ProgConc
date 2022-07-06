from threading import Lock
from Config.Singleton import Singleton


class MoonSupplySync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__moonNeedSupplies = False
            self.__moonSupplyMutex = Lock()

    @property
    def moonNeedSupplies(self) -> bool:
        return self.__moonNeedSupplies

    @moonNeedSupplies.setter
    def moonNeedSupplies(self, need: bool) -> None:
        self.__moonNeedSupplies = need

    @property
    def moonSupplyMutex(self) -> Lock:
        return self.__moonSupplyMutex
