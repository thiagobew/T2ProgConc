from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Bases, Planets, Rockets
from space.rocket import Rocket

import globals


class BaseLauncherThread(Thread):
    """Classe para controlar o setor de ataque de mísseis da base"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.__rocketInPlatform: Rocket = None

        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[BaseLauncher] -> Iniciando Departamento de Lançamento da base {self.base.name}')

        while (globals.get_release_system() == False):
            pass

        # O que limita lançamento de foguetes é a quantidade de recursos disponíveis
        # e se um foguete já ocupa a base, não podem 2 serem lançados ao mesmo tempo
        while True:
            # Posiciona um foguete na plataforma de lançamento quando disponível
            with self.base.storageMutex:
                if len(self.base.storage) == 0:
                    print(f'[{self.base.name}-Launcher] -> No Rockets, esperando...')
                    self.base.rocketInStorage.wait()

                self.__rocketInPlatform = self.base.storage.pop()

            # Efetua o lançamento do foguete
            self.__launchRocket()
            with self.base.storageMutex:
                print(f'[{self.base.name}-Launcher] -> Lançando foguete!')
                self.base.spaceForAnotherRocket.notify()

    def __launchRocket(self):
        if self.__rocketInPlatform.name == Rockets.LION:
            # self.__rocketInPlatform.voyage(Bases.MOON)
            pass
        else:
            destiny = self.__getRocketDestiny()
            # self.__rocketInPlatform.voyage(destiny)
            pass

    def __getRocketDestiny(self) -> Planets:
        return Planets.EUROPA
