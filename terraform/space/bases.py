from typing import List
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Bases, Rockets
from threading import BoundedSemaphore, Thread, Lock, Condition, Semaphore
from Synchronization.FinalizeSync import FinalizeSync
from space.BaseThreads.BaseEngineering import EarthBaseEngineeringThread
from space.BaseThreads.BaseLauncher import BaseLauncherThread
from space.BaseThreads.EarthBaseMining import EarthBaseMiningThread
from space.BaseThreads.MoonBaseEngineering import MoonBaseEngineeringThread
import globals


class SpaceBase(Thread, AbstractSpaceBase):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
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
        self.__rocketsStorageMutex = Lock()
        self.__semSpaceInStorage = BoundedSemaphore(self.__rocketsStorageLimit)
        self.__semRocketInStorage = Semaphore(0)

        # Cria as threads que irão trabalhar dentro da base, a base da Lua não possui departamento de Mineração
        if self.__name != Bases.MOON:
            self.baseEngineering = EarthBaseEngineeringThread(baseInstance=self, daemon=True)
            self.baseMining = EarthBaseMiningThread(baseInstance=self, daemon=True)
        else:
            self.baseEngineering = MoonBaseEngineeringThread(baseInstance=self, daemon=True)
        self.baseLauncher = BaseLauncherThread(baseInstance=self, daemon=True)

        # Inicia elas
        if self.__name != Bases.MOON:
            self.baseMining.start()
        self.baseEngineering.start()
        self.baseLauncher.start()

        globals.acquire_print()
        self.printSpaceBaseInfo()
        globals.release_print()

        # Espera a condição para o programa terminar
        with FinalizeSync().programFinishLock:
            FinalizeSync().programFinishCondition.wait()
        # Como as threads criadas pela Base são daemons irão ser finalizadas automaticamente

    def __getRocketsStorageLimit(self) -> int:
        if self.__name == Bases.ALCANTARA:
            return 1
        elif self.__name == Bases.MOON:
            return 2
        else:
            return 5

    def receiveLionRocket(self) -> None:
        # Método para ser usado pela base da Lua para guardar os recursos que chegaram do Lion
        if self.__name == Bases.MOON:
            self.baseEngineering.storeSuppliesOfLionRocket()

    def printSpaceBaseInfo(self):
        print(f"🔭 - [{self.__name}] → 🪨  {self.__uranium}/{self.__constraints[0]} URANIUM  ⛽ {self.fuel}/{self.__constraints[1]}  🚀 {len(self.__storage)}/{self.__constraints[2]}")

    @property
    def rocketsStorageMutex(self) -> Lock:
        return self.__rocketsStorageMutex

    @property
    def semRocketInStorage(self) -> Semaphore:
        return self.__semRocketInStorage

    @property
    def semSpaceInStorage(self) -> Semaphore:
        return self.__semSpaceInStorage

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
