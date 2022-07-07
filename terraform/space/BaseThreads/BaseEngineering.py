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

            # Espera pela quantidade necessária de recursos para criar foguete
            hasEnoughResources = False
            while not hasEnoughResources:
                # Adquire mutex para analisar o estoque
                with self.base.resourcesMutex:
                    # Verifica se precisa mandar suprimentos para a Lua
                    if self.moonSupplierIA.moonNeedSupplies:
                        hasEnoughResources = self.attackerIA.hasResourcesToCreateLion()
                    else:  # Ou atacar planetas
                        hasEnoughResources = self.attackerIA.hasResourcesToAttack()

                    # Se não tiver recursos necessários irá esperar
                    if not hasEnoughResources:
                        self.base.resourcesToCreateRockets.wait()

            # print(f'[{self.base.name} - Engineering] -> CRIANDO FOGUETE!!')
            # Acessa o estoque de recursos e cria o foguete
            with self.base.resourcesMutex:
                rocket = self.__createRocket()

            # Acessa o estoque de foguetes e armazena o foguete
            with self.base.storageMutex:
                self.base.storage.append(rocket)

            # Libera semáforo de foguete no estoque
            self.base.semRocketInStorage.release()

    def __createRocket(self) -> Rocket:
        if self.base.name != Bases.MOON and self.moonSupplierIA.moonNeedSupplies:
            return self.attackerIA.createRocketLion()

        return self.attackerIA.createRocketToAttack()
