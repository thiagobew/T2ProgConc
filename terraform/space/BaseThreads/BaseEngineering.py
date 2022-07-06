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
        print(f'[{self.base.name} - Engineering] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        while True:
            # Adquire o mutex para acessar o estoque de foguetes
            with self.base.storageMutex:
                if len(self.base.storage) == self.base.storageLimit:
                    print(f'[{self.base.name}-Engineering] -> NO SPACE FOR ROCKET!! Esperando...')
                    self.base.spaceForAnotherRocket.wait()

            # Adquire mutex para acessar os recursos
            with self.base.resourcesMutex:
                # Aguarda possuir recursos suficientes para criar Lion por meio de Condition
                if globals.moon_need_resources and self.base.name != Bases.MOON:
                    while not self.attackerIA.hasResourcesToCreateLion():
                        print(f'[{self.base.name}-Engineering] -> NO RESOURCES TO LION!!, esperando...')
                        self.base.resourcesToCreateRockets.wait()
                        continue

                # Aguarda possuir recursos suficientes para atacar por meio de Condition
                else:
                    while not self.attackerIA.hasResourcesToAttack():
                        print(f'[{self.base.name}-Engineering] -> NO RESOURCES TO ATTACK!!, esperando...')
                        self.base.resourcesToCreateRockets.wait()
                        continue

            print(f'[{self.base.name} - Engineering] -> CRIANDO FOGUETE!!')
            # Cria foguete necessário, adiciona ao estoque e notifica departamento de lançamento
            with self.base.storageMutex:
                self.base.storage.append(self.__createRocket())
                self.base.rocketInStorage.notify()

    def __createRocket(self) -> Rocket:
        if self.base.name != Bases.MOON and globals.moon_need_resources:
            return self.attackerIA.createRocketLion()

        return self.attackerIA.createRocketToAttack()
