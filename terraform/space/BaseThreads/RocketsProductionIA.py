from random import choice
from Enum.Enum import Bases, Rockets
from space.rocket import Rocket
from Abstractions.AbstractSpaceBase import AbstractSpaceBase


class RocketsProductionIA():
    def __init__(self, base: AbstractSpaceBase) -> None:
        self.base: AbstractSpaceBase = base

    def hasResourcesToAttack(self) -> bool:
        # Recursos para criar ogivas
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
        if self.hasResourcesToCreateDragon():
            rocketsToChoice.append(Rockets.DRAGON)
        if self.hasResourcesToCreateFalcon():
            rocketsToChoice.append(Rockets.FALCON)

        rocketName = choice(rocketsToChoice)
        if rocketName == Rockets.DRAGON:
            return self.createDragonRocket()
        else:
            return self.createFalconRocket()

    def hasResourcesToCreateLion(self) -> bool:
        # 75 para abastecer o Lion
        if (self.base.uranium < 75):
            return False

        minRequiredFuel = 0
        if self.base.name == Bases.ALCANTARA:
            minRequiredFuel = 220
        else:
            minRequiredFuel = 235

        if (self.base.fuel < minRequiredFuel):
            return False
        return True

    def createRocketLion(self) -> Rocket:
        self.base.uranium -= 75

        if self.base.name == Bases.ALCANTARA:
            self.base.fuel -= 220
        else:
            self.base.fuel -= 235

        if self.base.fuel < 0 or self.base.uranium < 0:
            print(f'❌ - [{self.base.name}] - Tentativa de criar Lion sem recursos necessários')
            return None

        return Rocket(Rockets.LION)

    def createFalconRocket(self) -> Rocket:
        self.base.uranium -= 35

        if self.base.name == Bases.ALCANTARA:
            self.base.fuel -= 100
        elif self.base.name == Bases.MOON:
            self.base.fuel -= 90
        else:
            self.base.fuel -= 120

        if self.base.fuel < 0 or self.base.uranium < 0:
            print(f'❌ - [{self.base.name}] - Tentativa de criar Falcon sem recursos necessários')
            return None

        return Rocket(Rockets.FALCON)

    def createDragonRocket(self) -> Rocket:
        self.base.uranium -= 35

        if self.base.name == Bases.ALCANTARA:
            self.base.fuel -= 70
        elif self.base.name == Bases.MOON:
            self.base.fuel -= 50
        else:
            self.base.fuel -= 100

        if self.base.fuel < 0 or self.base.uranium < 0:
            print(f'❌ - [{self.base.name}] - Tentativa de criar Dragon sem recursos necessários')
            return None

        return Rocket(Rockets.DRAGON)

    def hasResourcesToCreateDragon(self) -> bool:
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

    def hasResourcesToCreateFalcon(self) -> bool:
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
