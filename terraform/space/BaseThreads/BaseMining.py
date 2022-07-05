from threading import Thread
from Abstractions.AbstractSpaceBase import AbstractSpaceBase

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
            # Pega mutex para acessar os recursos da base e ver o que precisa
            with self.base.resourcesMutex:
                if self.base.uranium < self.base.uraniumLimit:
                    collectingUranium = True
                if self.base.fuel < self.base.fuelLimit:
                    collectingFuel = True

            if collectingFuel:
                self.__collectFuel()
            if collectingUranium:
                self.__collectUranium()

    def __collectFuel(self) -> None:
        pass

    def __collectUranium(self) -> None:
        pass
