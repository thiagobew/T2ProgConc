from enum import Enum


class Planets(Enum):
    IO = 'io'
    MARS = 'mars'
    GANIMEDES = 'ganimedes'
    EUROPA = 'europa'


class Rockets(Enum):
    DRAGON = 'Dragon'
    FALCON = 'Falcon'
    LION = 'Lion'


class Bases(Enum):
    ALCANTARA = 'alcantara'
    MOSCOW = 'moscow'
    CANAVERAL = 'canaveral_cape'
    MOON = 'moon'


class Mines(Enum):
    FUEL = 'oil_earth'
    URANIUM = 'uranium_earth'
