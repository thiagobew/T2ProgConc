from typing import List
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

        self.need_resources = False
        self.rockets_list: List[Rocket] = []

        while (globals.get_release_system() == False):
            pass

        # Só pode ser lançado um foguete por vez
        while True:
            if self.name == Bases.MOON:
                self.__earth_bases_run()
            else:
                self.__moon_bases_run()

    def __moon_bases_run(self):
        if self.uranium == 0 or self.fuel == 0:
            globals.moon_need_resources = True
        else:
            self.__attack_a_planet()

    def __earth_bases_run(self):
        if globals.moon_need_resources:
            self.__send_resources_to_moon()
        else:
            self.__attack_a_planet()

    def __send_resources_to_moon(self):
        rocket = self.__create_lion_rocket()
        if rocket is None:  # No resources for the rocket
            pass  # Coletar recurso de alguma base
        else:
            rocket.voyage(Bases.MOON)

    def __attack_a_planet(self):
        rocket_name = choice(Rockets.DRAGON, Rockets.FALCON)
        rocket = self.__create_rocket(rocket_name)

        if rocket is None:  # No resources for the rocket
            pass  # Coletar recurso de alguma base
        else:
            rocket.voyage()

    def __create_rocket(self, rocket_name: Rockets) -> Rocket:
        if rocket_name == Rockets.DRAGON:
            return self.__create_dragon_rocket()
        elif rocket_name == Rockets.FALCON:
            return self.__create_falcon_rocket()
        elif rocket_name == Rockets.LION:
            return self.__create_lion_rocket()
        else:
            print('Invalid rocket name')

    def __create_dragon_rocket(self) -> Rocket:
        if self.uranium > 35 and self.fuel > 50:
            self.uranium -= 35

            if self.name == Bases.ALCANTARA:
                self.fuel -= 70
            elif self.name == Bases.MOON:
                self.fuel -= 50
            else:
                self.fuel -= 100

            return Rocket(Rockets.DRAGON)
        return None

    def __create_falcon_rocket(self) -> Rocket:
        if self.uranium > 35 and self.fuel > 90:
            self.uranium -= 35

            if self.name == Bases.ALCANTARA:
                self.fuel -= 100
            elif self.name == Bases.MOON:
                self.fuel -= 90
            else:
                self.fuel -= 120

            return Rocket(Rockets.FALCON)
        return None

    def __create_lion_rocket(self) -> Rocket:
        if self.uranium > 35 and self.fuel > 100:
            self.uranium -= 35

            if self.name == Bases.ALCANTARA:
                self.fuel -= 100
            else:
                self.fuel -= 115

            return Rocket(Rockets.LION)
        return None

    def __refuel_oil(self):
        """Recarregar combustível, precisa adquirir o lock da mina de combustível e recarregar"""
        if (self.name == ''):
            pass

    def __refuel_uranium(self):
        """Recarregar urânio, precisa adquirir o lock da mina de urânio e recarregar"""
        pass

    def __print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")
