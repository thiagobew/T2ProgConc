from threading import Thread
from Abstractions.AbstractPlanet import AbstractPlanet
from Enum.Enum import Polo
import globals


class Planet(Thread, AbstractPlanet):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform, name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nukeDetected(self, damage: float, pole: Polo) -> None:
        self.terraform -= damage

        if pole == Polo.NORTH:
            print(
                f"💥 - [NUKE IN {self.name}] - North Pole was bombed by {damage:.5f}. {self.terraform}% UNINHABITABLE")
        else:
            print(
                f"💥 - [NUKE IN {self.name}] - South Pole was bombed by {damage:.5f}. {self.terraform}% UNINHABITABLE")

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
