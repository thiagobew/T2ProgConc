from Enum.Enum import Bases, Rockets
import globals
from threading import Thread
from space.rocket import Rocket
from random import choice


class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, uranium, fuel, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def run(self):
        globals.acquire_print()
        self.__print_space_base_info()
        globals.release_print()

        while (globals.get_release_system() == False):
            pass

        # Só pode ser lançado um foguete por vez
        while True:
            pass

    def base_rocket_resources(self, rocket: Rockets):
        if rocket == Rockets.DRAGON:
            self.__create_dragon_rocket()
        elif rocket == Rockets.FALCON:
            self.__create_falcon_rocket()
        elif rocket == Rockets.LION:
            self.__create_lion_rocket()
        else:
            print('Invalid rocket name')

    def __create_dragon_rocket(self):
        if self.uranium > 35 and self.fuel > 50:
            self.uranium -= 35

            if self.name == Bases.ALCANTARA:
                self.fuel -= 70
            elif self.name == Bases.MOON:
                self.fuel -= 50
            else:
                self.fuel -= 100

    def __create_falcon_rocket(self):
        if self.uranium > 35 and self.fuel > 90:
            self.uranium -= 35

            if self.name == Bases.ALCANTARA:
                self.fuel -= 100
            elif self.name == Bases.MOON:
                self.fuel -= 90
            else:
                self.fuel -= 120

    def __create_lion_rocket(self):
        if self.uranium > 35 and self.fuel > 100:
            self.uranium -= 35

            if self.name == Bases.ALCANTARA:
                self.fuel -= 100
            else:
                self.fuel -= 115

    def __refuel_oil(self):
        """Recarregar combustível, precisa adquirir o lock da mina de combustível e recarregar"""
        if (self.name == ''):
            pass

    def __refuel_uranium(self):
        """Recarregar urânio, precisa adquirir o lock da mina de urânio e recarregar"""
        pass

    def __print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")
