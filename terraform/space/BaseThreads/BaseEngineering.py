from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Synchronization.MoonResourcesSync import MoonSupplySync
from space.BaseThreads.RocketsProductionIA import RocketsProductionIA

import globals


class EarthBaseEngineeringThread(Thread):
    """Classe para a criação de foguetes para uma base"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.moonSupplierIA = MoonSupplySync()
        self.attackerIA = RocketsProductionIA(self.base)
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[{self.base.name} - ENGINEERING] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        while True:
            # Aguarda um lugar vazio no estoque de foguetes
            self.base.semSpaceInStorage.acquire()

            willSendLion = False
            if self.moonSupplierIA.moonNeedSupplies:
                # Tenta adquirir o mutex para ser a base a enviar um Lion para a Lua
                # Somente um planeta irá enviar um foguete para a Lua por vez
                willSendLion = self.moonSupplierIA.supplierSem.acquire(blocking=False)

            # Espera pela quantidade necessária de recursos para criar foguete
            hasEnoughResources = False
            with self.base.resourcesMutex:
                while not hasEnoughResources:
                    # Verifica se precisa mandar suprimentos para a Lua
                    if willSendLion:
                        hasEnoughResources = self.attackerIA.hasResourcesToCreateLion()
                    else:  # Ou atacar planetas
                        hasEnoughResources = self.attackerIA.hasResourcesToAttack()

                    # Se não tiver recursos necessários irá esperar chegar novos recursos
                    if not hasEnoughResources:
                        self.base.resourcesToCreateRockets.wait()

            # Acessa o estoque de recursos e cria o foguete
            with self.base.resourcesMutex:
                if willSendLion:
                    rocket = self.attackerIA.createRocketLion()
                else:
                    rocket = self.attackerIA.createRocketToAttack()

            # Acessa o estoque de foguetes e armazena o foguete
            with self.base.rocketsStorageMutex:
                self.base.storage.append(rocket)

            # Libera semáforo de foguete no estoque
            self.base.semRocketInStorage.release()
