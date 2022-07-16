from threading import BoundedSemaphore, Lock, Semaphore
from typing import Dict
from Config.Singleton import Singleton
import globals


class TerraformSync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__terraformMutexDic = {}
            self.__terraformSemaphoreDic = {}
            planets = globals.get_planets_ref()
            for key in planets:
                self.__terraformMutexDic[key] = Lock()
                self.__terraformSemaphoreDic[key] = BoundedSemaphore(2)

            # Semáforo para controlar a finalização do programa
            self.__semTerraformReady = Semaphore(0)

    @property
    def terraformMutexDic(self) -> Dict[str, Lock]:
        return self.__terraformMutexDic

    @property
    def terraformSemaphoreDic(self) -> Dict[str, BoundedSemaphore]:
        return self.__terraformSemaphoreDic

    @property
    def semTerraformReady(self) -> Semaphore:
        return self.__semTerraformReady
