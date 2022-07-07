from threading import Thread
from time import sleep
from typing import Tuple
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Bases, Planets, Polo, Rockets
from space.rocket import Rocket
from Synchronization.LaunchSync import LaunchSync
from Synchronization.PlanetsSync import PlanetsSync

import globals


class BaseLauncherThread(Thread):
    """Classe para controlar o setor de ataque de mísseis da base"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.__rocketInPlatform: Rocket = None
        self.__planets_ref = globals.get_planets_ref()

        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(
            f'[BaseLauncher] -> Iniciando Departamento de Lançamento da base {self.base.name}')

        while (globals.get_release_system() == False):
            pass

        # O que limita lançamento de foguetes é a quantidade de recursos disponíveis
        # e se um foguete já ocupa a base, não podem 2 serem lançados ao mesmo tempo
        while True:
            # Aguarda um foguete no estoque
            self.base.semRocketInStorage.acquire()

            # Remove o foguete do estoque e coloca na plataforma
            self.base.storageMutex.acquire()
            self.__rocketInPlatform = self.base.storage.pop(0)
            self.base.storageMutex.release()

            # Libera semáforo de espaço vazio no estoque
            self.base.semSpaceInStorage.release()

            # Efetua o lançamento do foguete
            voyageThread = Thread(target=self.__launchRocket)
            voyageThread.start()

    def __launchRocket(self):
        if self.__rocketInPlatform.name == Rockets.LION:
            print(f'[{self.base.name} - Launcher] -> Lançando Foguete para a Lua')
            moonBase = globals.get_bases_ref()['moon']

            self.__rocketInPlatform.voyage((moonBase,))
        else:
            print(f'[{self.base.name} - Launcher] -> Atacando planetas')
            return
            semFreePlanets = LaunchSync().semFreePlanets
            semFreePlanets.acquire()
            destiny = self.__getRocketDestiny()
            if(self.__rocketInPlatform.successfully_launch(self.base)):
                print(
                    f"[{self.__rocketInPlatform.name} - {self.__rocketInPlatform.id}] launched.")
                self.__rocketInPlatform.voyage(destiny)

    def __getRocketDestiny(self) -> Tuple[Planets, Polo]:
        planetsMutexes = PlanetsSync()
        for planet in self.__planets_ref:
            northFree = planetsMutexes.polesMutexDic[Polo.NORTH][planet].acquire(blocking=False)
            southFree = planetsMutexes.polesMutexDic[Polo.SOUTH][planet].acquire(blocking=False)

            if northFree:
                return (planet, Polo.NORTH)

            if southFree:
                return (planet, Polo.SOUTH)
