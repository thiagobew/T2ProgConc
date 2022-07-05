from threading import Lock
from Config.Singleton import Singleton


class MinesSync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__fuelMutex = Lock()
            self.__uraniumMutex = Lock()

    @property
    def fuelMineMutex(self) -> Lock:
        return self.__fuelMutex

    @property
    def uraniumMineMutex(self) -> Lock:
        return self.__uraniumMutex
