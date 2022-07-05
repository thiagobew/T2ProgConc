from threading import Lock
from typing import Dict
from Abstractions.AbstractMine import AbstractMine
from Abstractions.AbstractSpaceBase import AbstractSpaceBase
from Abstractions.AbstractPlanet import AbstractPlanet
from Enum.Enum import Bases, Mines, Planets

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las.
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

release_system = False
mutex_print = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None
moon_need_resources = False


def acquire_print() -> None:
    global mutex_print
    mutex_print.acquire()


def release_print() -> None:
    global mutex_print
    mutex_print.release()


def set_planets_ref(all_planets: Dict[Planets, AbstractPlanet]) -> None:
    global planets
    planets = all_planets


def get_planets_ref() -> Dict[Planets, AbstractPlanet]:
    global planets
    return planets


def set_bases_ref(all_bases: Dict[Bases, AbstractSpaceBase]) -> None:
    global bases
    bases = all_bases


def get_bases_ref() -> Dict[Bases, AbstractSpaceBase]:
    global bases
    return bases


def set_mines_ref(all_mines: Dict[Mines, AbstractMine]):
    global mines
    mines = all_mines


def get_mines_ref() -> Dict[Mines, AbstractMine]:
    global mines
    return mines


def set_release_system() -> None:
    global release_system
    release_system = True


def get_release_system() -> None:
    global release_system
    return release_system


def set_simulation_time(time: int) -> None:
    global simulation_time
    simulation_time = time


def get_simulation_time() -> int:
    global simulation_time
    return simulation_time
