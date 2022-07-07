from typing import List
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Bases, Rockets
from threading import BoundedSemaphore, Thread, Lock, Condition, Semaphore
from space.BaseThreads.BaseEngineering import EarthBaseEngineeringThread
from space.BaseThreads.BaseLauncher import BaseLauncherThread
from space.BaseThreads.EarthBaseMining import EarthBaseMiningThread
from space.BaseThreads.MoonBaseEngineering import MoonBaseEngineeringThread

import globals


class SpaceBase(Thread, AbstractSpaceBase):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, uranium, fuel, rockets):
        Thread.__init__(self)
        self.__name = name
        self.__uranium = 0
        self.__fuel = 0
        self.rockets = 0
        self.__constraints = [uranium, fuel, rockets]

    def run(self):
        self.__rocketsStorageLimit = self.__getRocketsStorageLimit()

        # Controle de concorrência para a mineração de recursos e criação de foguetes
        self.__resourcesMutex = Lock()
        self.__resourcesToCreateRockets = Condition(self.__resourcesMutex)
        self.__spaceInResourcesStorage = Condition(self.__resourcesMutex)

        # Controle de concorrência para a criação e lançamento de foguetes
        self.__storage: List[Rockets] = []
        self.__storageMutex = Lock()
        self.__spaceForAnotherRocket = Condition(self.__storageMutex)
        self.__rocketInStorage = Condition(self.__storageMutex)
        self.semSpaceInStorage = BoundedSemaphore(self.__rocketsStorageLimit)
        self.semRocketInStorage = Semaphore(0)

        # Cria as threads que irão trabalhar dentro da base
        if self.__name != Bases.MOON:
            self.baseEngineering = EarthBaseEngineeringThread(baseInstance=self)
            self.baseMining = EarthBaseMiningThread(baseInstance=self)
        else:
            self.baseEngineering = MoonBaseEngineeringThread(baseInstance=self)
        self.baseAttacker = BaseLauncherThread(baseInstance=self)

        # Inicia elas
        if self.__name != Bases.MOON:
            self.baseMining.start()
        self.baseEngineering.start()
        self.baseAttacker.start()

        globals.acquire_print()
        self.printSpaceBaseInfo()
        globals.release_print()

        # Espera pelas bases
        if self.__name != Bases.MOON:
            self.baseMining.join()
        self.baseEngineering.join()
        self.baseAttacker.join()

    def __getRocketsStorageLimit(self) -> int:
        if self.__name == Bases.ALCANTARA:
            return 1
        elif self.__name == Bases.MOON:
            return 2
        else:
            return 5

    def receiveLionRocket(self) -> None:
        if self.__name == Bases.MOON:
            self.baseEngineering.storeSuppliesOfLionRocket()

    def printSpaceBaseInfo(self):
        print(f"🔭 - [{self.__name}] → 🪨  {self.__uranium}/{self.__constraints[0]} URANIUM  ⛽ {self.fuel}/{self.__constraints[1]}  🚀 {len(self.__storage)}/{self.__constraints[2]}")

    @property
    def storageMutex(self) -> Lock:
        return self.__storageMutex

    @property
    def spaceForAnotherRocket(self) -> Condition:
        return self.__spaceForAnotherRocket

    @property
    def rocketInStorage(self) -> Condition:
        return self.__rocketInStorage

    @property
    def spaceInResourcesStorage(self) -> Condition:
        return self.__spaceInResourcesStorage

    @property
    def resourcesToCreateRockets(self) -> Condition:
        return self.__resourcesToCreateRockets

    @property
    def storage(self) -> List[Rockets]:
        return self.__storage

    @property
    def resourcesMutex(self) -> Lock:
        return self.__resourcesMutex

    @property
    def storageLimit(self) -> int:
        return self.__rocketsStorageLimit

    @property
    def uranium(self) -> int:
        return self.__uranium

    @uranium.setter
    def uranium(self, newUranium) -> None:
        self.__uranium = newUranium

    @property
    def fuel(self) -> int:
        return self.__fuel

    @fuel.setter
    def fuel(self, newFuel) -> None:
        self.__fuel = newFuel

    @property
    def fuelLimit(self) -> int:
        return self.__constraints[1]

    @property
    def uraniumLimit(self) -> int:
        return self.__constraints[0]

    @property
    def name(self) -> str:
        return self.__name
