from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Synchronization.MoonResourcesSync import MoonSupplySync
from space.BaseThreads.RocketsProductionIA import RocketsProductionIA

import globals


class MoonBaseEngineeringThread(Thread):
    """Classe para a criação de foguetes para uma base"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.moonSupplierIA = MoonSupplySync()
        self.rocketsIA = RocketsProductionIA(self.base)
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[{self.base.name} - ENGINEERING] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        while not globals.terraformReady:
            # Aguarda um lugar vazio no estoque de foguetes
            self.base.semSpaceInStorage.acquire()
            # print(
            # f'[MOON] - Tem lugar no estoque de foguetes - {self.base.storageLimit} - {len(self.base.storage)}')

            # Acessa o estoque e verifica se possui recursos suficientes, se não irá solicitar recursos e dormir
            hasEnoughResources = False
            while not hasEnoughResources:
                hasEnoughResources = self.rocketsIA.hasResourcesToAttack()

                # Se não possuir recursos espera
                if not hasEnoughResources:
                    with self.moonSupplierIA.moonSuppliesMutex:
                        self.moonSupplierIA.moonNeedSupplies = True
                        # Libera o semáforo para alguma base mandar um foguete para a Lua
                        self.moonSupplierIA.supplierSem.release()
                        self.moonSupplierIA.resourcesArrived.wait()

            # Já adquiriu recursos suficientes para construir Dragon
            self.moonSupplierIA.moonNeedSupplies = False

            # Adquire o mutex para acessar o estoque de suprimentos e o estoque de foguetes
            with self.base.resourcesMutex:
                with self.base.rocketsStorageMutex:
                    # Cria o foguete e adiciona ao estoque
                    self.base.storage.append(self.rocketsIA.createRocketToAttack())

            # Libera semáforo de foguete no estoque
            self.base.semRocketInStorage.release()

    def storeSuppliesOfLionRocket(self) -> None:
        print(f'🌑 ⛽ - [MOON] -> Lion aterrissando na Lua!')

        # Verifica quanto cabe no estoque
        spaceForFuel = self.base.fuelLimit - self.base.fuel
        spaceForUranium = self.base.uraniumLimit - self.base.uranium

        # Pega a quantidade que dá para armazenar
        fuelToStore = min(spaceForFuel, 120)
        uraniumToStore = min(spaceForUranium, 75)

        # Armazena os recursos
        with self.base.resourcesMutex:
            self.base.fuel += fuelToStore
            self.base.uranium += uraniumToStore
