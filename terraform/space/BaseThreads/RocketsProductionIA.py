from secrets import choice
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
        rocketName = choice(Rockets.DRAGON, Rockets.FALCON)
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
        if self.uranium > 35 and self.fuel > 100:
            self.uranium -= 35

            if self.name == Bases.ALCANTARA:
                self.fuel -= 100
            else:
                self.fuel -= 115

            return Rocket(Rockets.LION)
        return None

    def __createFalconRocket(self) -> Rocket:
        self.base.uranium -= 35

        if self.name == Bases.ALCANTARA:
            self.base.fuel -= 100
        elif self.name == Bases.MOON:
            self.base.fuel -= 90
        else:
            self.base.fuel -= 120

        return Rocket(Rockets.FALCON)

    def __createDragonRocket(self) -> Rocket:
        self.uranium -= 35

        if self.name == Bases.ALCANTARA:
            self.fuel -= 70
        elif self.name == Bases.MOON:
            self.fuel -= 50
        else:
            self.fuel -= 100

        return Rocket(Rockets.DRAGON)
