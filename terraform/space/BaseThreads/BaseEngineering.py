from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Bases
from Synchronization.MoonResourcesSync import MoonSupplySync
from space.BaseThreads.RocketsProductionIA import RocketsProductionIA
from space.rocket import Rocket

import globals


class EarthBaseEngineeringThread(Thread):
    """Classe para a criação de foguetes para uma base"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.moonSupplierIA = MoonSupplySync()
        self.attackerIA = RocketsProductionIA(self.base)
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[{self.base.name} - Engineering] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        while True:
            # Aguarda um lugar vazio no estoque de foguetes
            self.base.semSpaceInStorage.acquire()

            # Adquire mutex para acessar os recursos
            # Ele é notificado sempre que novos recursos são adicionados, por isso o mecanismo while not e continue
            # para quando ele acordar verificar se já existe recursos suficientes e prosseguir com a criação
            with self.base.resourcesMutex:
                # Aguarda possuir recursos suficientes para criar Lion por meio de Condition
                if self.moonSupplierIA.moonNeedSupplies and self.base.name != Bases.MOON:
                    while not self.attackerIA.hasResourcesToCreateLion():
                        # print(f'[{self.base.name}-Engineering] -> NO RESOURCES TO LION!!, esperando...')
                        self.base.resourcesToCreateRockets.wait()
                        continue

                # Aguarda possuir recursos suficientes para atacar por meio de Condition
                else:
                    while not self.attackerIA.hasResourcesToAttack():
                        # print(f'[{self.base.name}-Engineering] -> NO RESOURCES TO ATTACK!!, esperando...')
                        self.base.resourcesToCreateRockets.wait()
                        continue

            # print(f'[{self.base.name} - Engineering] -> CRIANDO FOGUETE!!')
            # Cria foguete e adiciona ao estoque
            self.base.resourcesMutex.acquire()
            self.base.storage.append(self.__createRocket())
            self.base.resourcesMutex.release()

            # Libera semáforo de foguete no estoque
            self.base.semRocketInStorage.release()

    def __createRocket(self) -> Rocket:
        if self.base.name != Bases.MOON and self.moonSupplierIA.moonNeedSupplies:
            return self.attackerIA.createRocketLion()

        return self.attackerIA.createRocketToAttack()
