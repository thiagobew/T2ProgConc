from threading import Thread, Lock
from Abstractions.AbstractPlanet import AbstractPlanet
from Synchronization import LaunchSync
import globals


class Planet(Thread, AbstractPlanet):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform, name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nukeDetected(self, damage, lock):
        self.terraform -= damage
        lock.release()
        print(
            f"[NUKE DETECTION] - The planet {self.name} was bombed by {damage}. {self.terraform}% UNHABITABLE")
        semFreePlanets = LaunchSync().semFreePlanets
        semFreePlanets.release()

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
