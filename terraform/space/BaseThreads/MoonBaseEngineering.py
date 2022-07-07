from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Bases
from Synchronization.MoonResourcesSync import MoonSupplySync
from space.BaseThreads.RocketsProductionIA import RocketsProductionIA
from space.rocket import Rocket

import globals


class MoonBaseEngineeringThread(Thread):
    """Classe para a criação de foguetes para uma base"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.moonSupplierIA = MoonSupplySync()
        self.rocketsIA = RocketsProductionIA(self.base)
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[{self.base.name} - Engineering] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        while True:
            # Aguarda um lugar vazio no estoque de foguetes
            self.base.semSpaceInStorage.acquire()

            # Acessa o estoque e verifica se possui recursos suficientes, se não irá solicitar recursos e dormir
            hasEnoughResources = False
            while not hasEnoughResources:
                hasEnoughResources = self.rocketsIA.hasResourcesToCreateDragon()

                # Se não possuir recursos espera
                if not hasEnoughResources:
                    with self.moonSupplierIA.moonSupplyMutex:
                        self.moonSupplierIA.moonNeedSupplies = True
                        self.moonSupplierIA.resourcesArrived.wait()

            # Já adquiriu recursos suficientes para construir Dragon
            self.moonSupplierIA.moonNeedSupplies = False

            # Cria foguete e adiciona ao estoque
            self.base.storage.append(self.__createRocket())

            # Libera semáforo de foguete no estoque
            self.base.semRocketInStorage.release()

    def __createRocket(self) -> Rocket:
        if self.base.name != Bases.MOON and self.moonSupplierIA.moonNeedSupplies:
            return self.rocketsIA.createRocketLion()

        return self.rocketsIA.createRocketToAttack()