from threading import Lock, Semaphore
from typing import Dict
from Config.Singleton import Singleton
import globals


class TerraformSync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__terraformMutexDic = {}
            planets = globals.get_planets_ref()
            for key in planets:
                self.__terraformMutexDic[key] = Lock()

            # Semáforo para controlar a finalização do programa
            self.__semTerraformReady = Semaphore(0)

    @property
    def terraformMutexDic(self) -> Dict[str, Lock]:
        return self.__terraformMutexDic

    @property
    def semTerraformReady(self) -> Semaphore:
        return self.__semTerraformReady
