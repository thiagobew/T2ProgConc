from threading import Thread
from time import sleep
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Synchronization.MinesSync import MinesSync

import globals


class BaseMiningThread(Thread):
    """Classe para controlar o processo de mineração para uma base espacial"""

    def __init__(self, baseInstance: AbstractSpaceBase, target=None, name=None, args=None,  kwargs=None, daemon=None) -> None:
        self.base: AbstractSpaceBase = baseInstance
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'[BaseMining] -> Iniciando Departamento de Mineração de {self.base.name}')

        while (globals.get_release_system() == False):
            pass

        while True:
            collectingUranium = False
            collectingFuel = False
            fuelRequired = 0
            uraniumRequired = 0
            # Pega mutex para acessar os recursos da base e ver o que precisa
            with self.base.resourcesMutex:
                if self.base.uranium < self.base.uraniumLimit:
                    collectingUranium = True
                    uraniumRequired = self.base.uraniumLimit - self.base.uranium
                if self.base.fuel < self.base.fuelLimit:
                    collectingFuel = True
                    fuelRequired = self.base.fuelLimit - self.base.fuel

            if collectingFuel:
                self.__collectFuel(fuelRequired)
            if collectingUranium:
                self.__collectUranium(uraniumRequired)

    def __collectFuel(self, fuelRequired: int) -> None:
        # Entra na região crítica e pega a mina de fuel
        MinesSync().fuelMineMutex.acquire()
        fuelMine = globals.get_mines_ref()['oil_earth']

        globals.acquire_print()
        print(f'Mining da base {self.base.name} está consumindo a mina de fuel')
        globals.release_print()

        # Verifica quanto de fuel é possível extrair
        quantToExtract = min(fuelRequired, fuelMine.unities)
        fuelMine.unities -= quantToExtract

        globals.acquire_print()
        print(f'Mining da base {self.base.name} liberou a mina')
        globals.release_print()
        sleep(3)

        # Libera a mina de fuel
        MinesSync().fuelMineMutex.release()

        # Alimenta o estoque de fuel da base
        with self.base.resourcesMutex:
            self.base.fuel += quantToExtract

        print(f'BASE: [{self.base.name}] - FUEL: {self.base.fuel}')

    def __collectUranium(self, requiredUranium: int) -> None:
        uraniumMine = globals.get_mines_ref()['uranium_earth']
        pass
