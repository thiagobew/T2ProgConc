from threading import Thread
from typing import Tuple
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Planets, Polo, Rockets
from Synchronization.MoonResourcesSync import MoonSupplySync
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
        print(f'[{self.base.name} LAUNCHER] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        # O que limita lançamento de foguetes é a quantidade de recursos disponíveis
        # e se um foguete já ocupa a base, não podem 2 serem lançados ao mesmo tempo
        while True:
            # Aguarda um foguete no estoque
            self.base.semRocketInStorage.acquire()

            # print(f'[{self.base.name} - Launcher] -> Removendo foguete do Estoque')
            # Remove o foguete do estoque e coloca na plataforma
            self.base.rocketsStorageMutex.acquire()
            self.__rocketInPlatform = self.base.storage.pop(0)
            self.base.rocketsStorageMutex.release()

            # Libera semáforo de espaço vazio no estoque
            self.base.semSpaceInStorage.release()

            # Verifica se teve um lançamento com sucesso a ativa a Thread para cuidar do voyage
            if self.__rocketInPlatform.successfully_launch(self.base):
                voyageThread = Thread(target=self.__voyageRocket, args=(self.__rocketInPlatform,))
                voyageThread.start()
            else:  # Se rocket falhado foi Lion libera para outra base tentar enviar o Lion também
                if self.__rocketInPlatform.name == Rockets.LION:
                    MoonSupplySync().supplierSem.release()

    def __voyageRocket(self, rocket: Rocket):
        """Função que controla a viagem do foguete"""
        if rocket.name == Rockets.LION:
            print(f'🚀🌑 - [{self.base.name} - Launcher] -> Foguete lançado para a Lua')
            moonBase = globals.get_bases_ref()['moon']

            rocket.voyage((moonBase,))
        else:
            print(f'🚀🪐 - [{self.base.name} - Launcher] -> Foguete lançado contra planetas')
            return
            semFreePlanets = LaunchSync().semFreePlanets
            semFreePlanets.acquire()
            destiny = self.__getRocketDestiny()
            if(rocket.successfully_launch(self.base)):
                print(
                    f"[{rocket.name} - {rocket.id}] launched.")
                rocket.voyage(destiny)

    def __getRocketDestiny(self) -> Tuple[Planets, Polo]:
        planetsMutexes = PlanetsSync()
        for planet in self.__planets_ref:
            northFree = planetsMutexes.polesMutexDic[Polo.NORTH][planet].acquire(blocking=False)
            southFree = planetsMutexes.polesMutexDic[Polo.SOUTH][planet].acquire(blocking=False)

            if northFree:
                return (planet, Polo.NORTH)

            if southFree:
                return (planet, Polo.SOUTH)
