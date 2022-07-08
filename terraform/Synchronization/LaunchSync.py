from threading import Semaphore
from Config.Singleton import Singleton
import globals


class LaunchSync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            planetsAmount = len(globals.get_planets_ref())

            # Semáforo para indicar se há algum polo livre para lançamento
            self.__semFreePlanets = Semaphore(planetsAmount * 2)

    @property
    def semFreePlanets(self) -> Semaphore:
        return self.__semFreePlanets
