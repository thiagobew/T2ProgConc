from threading import Thread
from time import sleep
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

            # Remove o planeta destruído do dicionário de planetas não destruídos
            dicNoTerraformedPlanets = globals.getNoTerraformedPlanets()
            nameToDelete = self.name.lower()
            del dicNoTerraformedPlanets[nameToDelete]

            # Libera um contador do Terraform Verifier
            TerraformSync().semTerraformReady.release()
            return True

        # Essa alteração do valor já está protegido por um Lock adquirido antes da chamada desse método
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

        globals.acquire_print()
        self.printPlanetInfo()
        globals.release_print()

        while (globals.get_release_system() == False):
            pass

        while not globals.getTerraformReady():
            # Somente fica dando print do terraform
            sleep(1)
            self.printPlanetInfo()
