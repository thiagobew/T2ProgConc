from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Bases
from space.BaseThreads.RocketsProductionIA import RocketsProductionIA
from space.rocket import Rocket

import globals


class BaseEngineeringThread(Thread):
    """Classe para a criação de foguetes para uma base"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.attackerIA = RocketsProductionIA(self.base)
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[BaseEngineering] -> Iniciando Departamento de Engenharia da base {self.base.name}')

        while (globals.get_release_system() == False):
            pass

        while True:
            # Adquire mutex para acessar os recursos
            with self.base.resourcesMutex:
                if not self.attackerIA.hasResourcesToAttack():
                    print(f'[BaseEngineering] -> Sem recursos para criar foguete, esperando...')
                    self.base.resourcesToCreateRockets.wait()

                # Adquire o mutex para acessar o estoque de foguetes
                with self.base.storageMutex:
                    if len(self.base.storage) == self.base.storageLimit:
                        print(f'[BaseEngineering] -> Sem espaço para criar foguete, esperando...')
                        self.base.spaceForAnotherRocket.wait()

                    self.base.storage.append(self.__createRocket())

    def __createRocket(self) -> Rocket:
        if self.base.name != Bases.MOON and globals.moon_need_resources:
            return self.attackerIA.createRocketLion()

        return self.attackerIA.createRocketToAttack()
