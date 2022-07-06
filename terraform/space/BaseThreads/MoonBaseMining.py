from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Synchronization.MoonResourcesSync import MoonSupplySync

import globals
from space.BaseThreads.RocketsProductionIA import RocketsProductionIA


class MoonBaseMiningThread(Thread):
    """Classe para controlar o processo de coleta de recursos para uma base espacial na lua"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        self.rocketsIA = RocketsProductionIA(self.base)
        self.moonSupplyIA = MoonSupplySync()
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[{self.base.name} - MINING] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        while True:
            # Pega mutex para acessar os recursos da base e ver se precisa de recursos
            with self.base.resourcesMutex:
                # Caso estoque lotado espera os recursos serem consumidos
                if self.base.uranium >= self.base.uraniumLimit and self.base.fuel >= self.base.fuelLimit:
                    self.moonSupplyIA.moonNeedSupplies = False
                    self.base.spaceInResourcesStorage.wait()
                    continue

            self.moonSupplyIA.moonNeedSupplies = True

    def storeSuppliesOfLionRocket(self) -> None:
        spaceForFuel = self.base.fuelLimit - self.base.fuel
        spaceForUranium = self.base.uraniumLimit - self.base.uranium

        fuelToStore = min(spaceForFuel, 120)
        uraniumToStore = min(spaceForUranium, 75)

        with self.base.resourcesMutex:
            self.base.fuel += fuelToStore
            self.base.uranium += uraniumToStore

            self.base.resourcesToCreateRockets.notify()
