from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Enum.Enum import Mines
from Synchronization.MinesSync import MinesSync

import globals


class EarthBaseMiningThread(Thread):
    """Classe para controlar o processo de mineração para uma base espacial na terra"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[{self.base.name} - MINING] -> Iniciando operações')

        while (globals.get_release_system() == False):
            pass

        while not globals.getTerraformReady():
            spaceAvailableForUranium = False
            spaceAvailableForFuel = False
            fuelRequired = 0
            uraniumRequired = 0
            # Pega mutex para acessar os recursos da base e ver o que precisa
            with self.base.resourcesMutex:
                # Caso estoque lotado espera os recursos serem consumidos
                if self.base.uranium >= self.base.uraniumLimit and self.base.fuel >= self.base.fuelLimit:
                    self.base.spaceInResourcesStorage.wait()
                    continue

                # Verifica quanto de uranium ainda cabe no estoque
                if self.base.uranium < self.base.uraniumLimit:
                    spaceAvailableForUranium = True
                    uraniumRequired = self.base.uraniumLimit - self.base.uranium

                # Verifica quanto de combustível ainda cabe no estoque
                if self.base.fuel < self.base.fuelLimit:
                    spaceAvailableForFuel = True
                    fuelRequired = self.base.fuelLimit - self.base.fuel

            # Se necessário coleta combustível
            if spaceAvailableForFuel:
                collectedFuel = self.__collectFuel(fuelRequired)
                self.__storeFuel(collectedFuel)

            # Se necessário coleta urânio
            if spaceAvailableForUranium:
                collectedUranium = self.__collectUranium(uraniumRequired)
                self.__storeUranium(collectedUranium)

    def __collectFuel(self, fuelRequired: int) -> int:
        # Entra na região crítica e pega a mina de fuel
        MinesSync().fuelMineMutex.acquire()
        fuelMine = globals.get_mines_ref()[Mines.FUEL]

        # Verifica quanto de fuel é possível extrair e armazenar
        quantToExtract = min(fuelRequired, fuelMine.unities)
        fuelMine.unities -= quantToExtract

        # Libera a mina de fuel
        MinesSync().fuelMineMutex.release()

        return quantToExtract

    def __collectUranium(self, requiredUranium: int) -> int:
        # Entra na região crítica e pega a mina de fuel
        MinesSync().uraniumMineMutex.acquire()
        uraniumMine = globals.get_mines_ref()[Mines.URANIUM]

        # Verifica quanto de fuel é possível extrair
        quantToExtract = min(requiredUranium, uraniumMine.unities)
        uraniumMine.unities -= quantToExtract

        # Libera a mina de fuel
        MinesSync().uraniumMineMutex.release()

        return quantToExtract

    def __storeFuel(self, fuelCollected: int) -> None:
        if fuelCollected == 0:
            return

        # Alimenta o estoque de fuel da base
        with self.base.resourcesMutex:
            self.base.fuel += fuelCollected
            # Notifica o departamento de lançamento de foguetes que houve alteração nos recursos
            self.base.resourcesToCreateRockets.notify()

    def __storeUranium(self, uraniumCollected: int) -> None:
        if uraniumCollected == 0:
            return

        # Alimenta o estoque de fuel da base
        with self.base.resourcesMutex:
            self.base.uranium += uraniumCollected
            # Notifica o departamento de lançamento de foguetes que houve alteração nos recursos
            self.base.resourcesToCreateRockets.notify()
