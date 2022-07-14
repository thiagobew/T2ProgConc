from threading import Thread
from Abstractions.AbstractPlanet import AbstractPlanet
from Enum.Enum import Polo
import globals
from Synchronization.TerraformSync import TerraformSync


class Planet(Thread, AbstractPlanet):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform, name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nukeDetected(self, damage: float, pole: Polo) -> bool:
        # Impede que um foguete lance uma bomba se o planeta já foi terraformado
        if self.terraform == 0:
            return True

        if self.terraform <= damage:
            print('=-=' * 30)
            print(f'PLANET {self.name} WAS SUCCESSFULLY TERRAFORMED')
            print('=-=' * 30)
            self.terraform = 0
            dicNoTerraformedPlanets = globals.getNoTerraformedPlanets()
            nameToDelete = self.name.lower()
            del dicNoTerraformedPlanets[nameToDelete]
            TerraformSync().semTerraformReady.release()
            return True

        self.terraform -= damage

        if pole == Polo.NORTH:
            print(
                f"💥 - [NUKE IN {self.name}] - North Pole was bombed by {damage:.5f}. {self.terraform}% UNINHABITABLE")
        else:
            print(
                f"💥 - [NUKE IN {self.name}] - South Pole was bombed by {damage:.5f}. {self.terraform}% UNINHABITABLE")

        return False

    def printPlanetInfo(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        # Criando mutex para proteger int terraform
        planets = globals.get_planets_ref()
        # planets[self.name]["terraformMutex"] = Lock()

        globals.acquire_print()
        self.printPlanetInfo()
        globals.release_print()

        while (globals.get_release_system() == False):
            pass
