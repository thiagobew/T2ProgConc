from threading import Condition, Lock
from Config.Singleton import Singleton


class MoonSupplySync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__moonNeedSupplies = False
            self.__moonSupplyMutex = Lock()
            self.__resourcesArrived = Condition(self.__moonSupplyMutex)

    @property
    def moonNeedSupplies(self) -> bool:
        return self.__moonNeedSupplies

    @moonNeedSupplies.setter
    def moonNeedSupplies(self, need: bool) -> None:
        self.__moonNeedSupplies = need

    @property
    def moonSupplyMutex(self) -> Lock:
        return self.__moonSupplyMutex

    @property
    def resourcesArrived(self) -> Condition:
        return self.__resourcesArrived
