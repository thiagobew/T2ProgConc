from threading import BoundedSemaphore, Condition, Lock, Semaphore
from Config.Singleton import Singleton


class MoonSupplySync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__moonNeedSupplies = False
            self.__moonSuppliesMutex = Lock()
            self.__supplierSem = Semaphore(0)
            self.__resourcesArrived = Condition(self.__moonSuppliesMutex)

    @property
    def moonNeedSupplies(self) -> bool:
        return self.__moonNeedSupplies

    @moonNeedSupplies.setter
    def moonNeedSupplies(self, need: bool) -> None:
        self.__moonNeedSupplies = need

    @property
    def moonSuppliesMutex(self) -> Lock:
        return self.__moonSuppliesMutex

    @property
    def supplierSem(self) -> Semaphore:
        return self.__supplierSem

    @property
    def resourcesArrived(self) -> Condition:
        return self.__resourcesArrived
