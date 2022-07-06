from random import choice
from Enum.Enum import Bases, Rockets
from space.rocket import Rocket
from Abstractions.AbstractSpaceBase import AbstractSpaceBase


class RocketsProductionIA():
    def __init__(self, base: AbstractSpaceBase) -> None:
        self.base: AbstractSpaceBase = base

    def hasResourcesToAttack(self) -> bool:
        if (self.base.uranium < 35):
            return False

        minRequiredFuel = 0
        if (self.base.name == Bases.MOON):
            minRequiredFuel = 50
        elif (self.base.name == Bases.ALCANTARA):
            minRequiredFuel = 70
        else:
            minRequiredFuel = 100

        if (self.base.fuel < minRequiredFuel):
            return False
        return True

    def createRocketToAttack(self) -> Rocket:
        rocketsToChoice = []
        if self.__hasResourcesToCreateDragon():
            rocketsToChoice.append(Rockets.DRAGON)
        if self.__hasResourcesToCreateFalcon():
            rocketsToChoice.append(Rockets.FALCON)

        rocketName = choice(rocketsToChoice)
        if rocketName == Rockets.DRAGON:
            return self.__createDragonRocket()
        else:
            return self.__createFalconRocket()

    def hasResourcesToCreateLion(self) -> bool:
        if (self.base.uranium < 35):
            return False

        minRequiredFuel = 0
        if self.base.name == Bases.ALCANTARA:
            minRequiredFuel = 100
        else:
            minRequiredFuel = 115

        if (self.base.fuel < minRequiredFuel):
            return False
        return True

    def createRocketLion(self) -> Rocket:
        if self.base.uranium < 35 or self.base.fuel < 100:
            print(f'[ERRO] - [{self.base.name}] - Tentativa de criar Lion sem recursos necessários')
            return None

        self.base.uranium -= 35

        if self.base.name == Bases.ALCANTARA:
            self.base.fuel -= 100
        else:
            self.base.fuel -= 115

        return Rocket(Rockets.LION)

    def __createFalconRocket(self) -> Rocket:
        self.base.uranium -= 35

        if self.base.name == Bases.ALCANTARA:
            self.base.fuel -= 100
        elif self.base.name == Bases.MOON:
            self.base.fuel -= 90
        else:
            self.base.fuel -= 120

        return Rocket(Rockets.FALCON)

    def __createDragonRocket(self) -> Rocket:
        self.base.uranium -= 35

        if self.base.name == Bases.ALCANTARA:
            self.base.fuel -= 70
        elif self.base.name == Bases.MOON:
            self.base.fuel -= 50
        else:
            self.base.fuel -= 100

        return Rocket(Rockets.DRAGON)

    def __hasResourcesToCreateDragon(self) -> bool:
        if self.base.uranium < 35:
            return False

        requiredFuel = 0
        if self.base.name == Bases.ALCANTARA:
            requiredFuel = 70
        elif self.base.name == Bases.MOON:
            requiredFuel = 50
        else:
            requiredFuel = 100

        if self.base.fuel < requiredFuel:
            return False
        return True

    def __hasResourcesToCreateFalcon(self) -> bool:
        if self.base.uranium < 35:
            return False

        requiredFuel = 0
        if self.base.name == Bases.ALCANTARA:
            requiredFuel = 100
        elif self.base.name == Bases.MOON:
            requiredFuel = 90
        else:
            requiredFuel = 120

        if self.base.fuel < requiredFuel:
            return False
        return True
