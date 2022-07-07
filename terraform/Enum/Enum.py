from enum import Enum


class Planets(str, Enum):
    IO = 'io'
    MARS = 'mars'
    GANIMEDES = 'ganimedes'
    EUROPA = 'europa'


class Rockets(str, Enum):
    DRAGON = 'Dragon'
    FALCON = 'Falcon'
    LION = 'Lion'


class Bases(str, Enum):
    ALCANTARA = 'ALCANTARA'
    MOSCOW = 'MOSCOW'
    CANAVERAL = 'CANAVERAL CAPE'
    MOON = 'MOON'


class Mines(str, Enum):
    FUEL = 'oil_earth'
    URANIUM = 'uranium_earth'


class Polo(str, Enum):
    NORTH = 'north'
    SOUTH = 'south'
