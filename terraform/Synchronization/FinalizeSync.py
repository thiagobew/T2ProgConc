from threading import Lock, Condition
from Config.Singleton import Singleton


class FinalizeSync(Singleton):
    def __init__(self) -> None:
        if not super().created:
            self.__programFinishLock = Lock()
            self.__programFinishCondition = Condition(self.__programFinishLock)

    @property
    def programFinishCondition(self) -> Condition:
        return self.__programFinishCondition

    @property
    def programFinishLock(self) -> Lock:
        return self.__programFinishLock
