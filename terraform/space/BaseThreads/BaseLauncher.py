from random import choice
from threading import Thread
from Abstractions.AbstractPlanet import AbstractPlanet
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Rockets
from Synchronization.MoonResourcesSync import MoonSupplySync
from space.rocket import Rocket

import globals


class BaseLauncherThread(Thread):
    """Classe para controlar o setor de ataque de mísseis da base"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.__rocketInPlatform: Rocket = None

        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[{self.base.name} LAUNCHER] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        # O que limita lançamento de foguetes é a quantidade de recursos disponíveis
        # e se um foguete já ocupa a base, não podem 2 serem lançados ao mesmo tempo
        while not globals.getTerraformReady():
            # Aguarda um foguete no estoque
            self.base.semRocketInStorage.acquire()

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
            else:  # Se o rocket que falhou foi Lion libera para outra base tentar enviar o Lion também
                if self.__rocketInPlatform.name == Rockets.LION:
                    MoonSupplySync().supplierSem.release()

    def __voyageRocket(self, rocket: Rocket):
        """Função que controla a viagem do foguete"""
        if rocket.name == Rockets.LION:
            print(f'🚀 🌑 - [{self.base.name} - Launcher] -> Foguete lançado para a Lua')
            moonBase = globals.get_bases_ref()['moon']

            rocket.voyage(moonBase)
        else:
            destiny = self.__getRocketDestiny()
            if destiny is not None:
                print(
                    f'🚀 🪐 - [{self.base.name} - Launcher] -> Foguete lançado em direção ao planeta {destiny.name}')
                rocket.voyage(destiny)

    def __getRocketDestiny(self) -> AbstractPlanet:
        # Escolhe aleatoriamente um dos planetas ainda não terraformados
        planetsDict = globals.getNoTerraformedPlanets()

        # Caso todos os planetas foram terraformados e não tem mais destinos
        if len(planetsDict) == 0:
            return None

        chosen = choice(list(planetsDict.keys()))
        return planetsDict[chosen]
