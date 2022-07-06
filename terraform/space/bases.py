from typing import List
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Bases, Rockets
from threading import Thread, Lock, Condition
from space.BaseThreads.BaseEngineering import BaseEngineeringThread
from space.BaseThreads.BaseLauncher import BaseLauncherThread
from space.BaseThreads.EarthBaseMining import EarthBaseMiningThread
from space.BaseThreads.MoonBaseMining import MoonBaseMiningThread

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
        self.__maximumStorageRockets = self.__getRocketsStorageLimit()

        # Controle de concorrência para a mineração de recursos e criação de foguetes
        self.__resourcesMutex = Lock()
        self.__resourcesToCreateRockets = Condition(self.__resourcesMutex)
        self.__spaceInResourcesStorage = Condition(self.__resourcesMutex)

        # Controle de concorrência para a criação e lançamento de foguetes
        self.__storage: List[Rockets] = []
        self.__storageMutex = Lock()
        self.__spaceForAnotherRocket = Condition(self.__storageMutex)
        self.__rocketInStorage = Condition(self.__storageMutex)

        # Cria as threads que irão trabalhar dentro da base
        if self.__name == Bases.MOON:
            self.baseMining = MoonBaseMiningThread(baseInstance=self)
        else:
            self.baseMining = EarthBaseMiningThread(baseInstance=self)
        self.baseAttacker = BaseLauncherThread(baseInstance=self)
        self.baseEngineering = BaseEngineeringThread(baseInstance=self)

        # Inicia elas
        self.baseMining.start()
        self.baseAttacker.start()
        self.baseEngineering.start()

        globals.acquire_print()
        self.printSpaceBaseInfo()
        globals.release_print()

        # Espera pelas bases
        self.baseMining.join()
        self.baseAttacker.join()
        self.baseEngineering.join()

    def __getRocketsStorageLimit(self) -> int:
        if self.__name == Bases.ALCANTARA:
            return 1
        elif self.__name == Bases.MOON:
            return 2
        else:
            return 5

    def receiveLionRocket(self) -> None:
        if self.__name == Bases.MOON:
            self.baseMining.storeSuppliesOfLionRocket()

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
        return self.__maximumStorageRockets

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
