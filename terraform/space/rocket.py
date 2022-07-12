from random import randrange, random
from time import sleep
from typing import Tuple
from Abstractions.AbstractPlanet import AbstractPlanet
from Synchronization.MoonResourcesSync import MoonSupplySync
from Synchronization.TerraformSync import TerraformSync
import globals
from Enum.Enum import Polo, Rockets
from Synchronization.PlanetsSync import PlanetsSync
from Synchronization.LaunchSync import LaunchSync


class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if (self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0

    # Permitida a alteração
    def nuke(self, planetAndPole: Tuple[AbstractPlanet, Polo]):
        planet = planetAndPole[0]
        pole = planetAndPole[1]

        # Pega o nome do planeta em minúsculo para conseguir acessar o dicionário criado em simulation
        planetName = planet.name.lower()
        # Adquire e depois solta o mutex para alterar o terraform do planeta
        TerraformSync().terraformMutexDic[planetName].acquire()
        done = planet.nukeDetected(self.damage(), pole)
        TerraformSync().terraformMutexDic[planetName].release()

        if not done:
            # Libera um no semáforo de destinos disponíveis para atacar
            LaunchSync().semFreePlanets.release()
            # Libera o mutex do destino específico, o polo que foi atacado
            PlanetsSync().polesMutexDic[pole][planetName].release()

    def voyage(self, planetAndPole: Tuple):  # Permitida a alteração (com ressalvas)
        if self.name == Rockets.LION:
            # Nesse caso, o planeta é a base lunar
            moonBase = planetAndPole[0]
            moonSupplyIA = MoonSupplySync()

            # 4 dias de viagem
            sleep(0.011)

            # talvez nunca há problemas na viagem para a Lua?
            # self.do_we_have_a_problem()

            # Armazena suprimentos no estoque
            moonBase.receiveLionRocket()

            # Notifica departamento de engenharia da Lua que tem novos recursos
            with moonSupplyIA.moonSuppliesMutex:
                moonSupplyIA.resourcesArrived.notify()
        else:
            # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
            # Você pode inserir código antes ou depois dela e deve
            # usar essa função.
            self.simulation_time_voyage(planetAndPole[0])
            failure = self.do_we_have_a_problem()
            if failure:
                LaunchSync().semFreePlanets.release()
                PlanetsSync().polesMutexDic[planetAndPole[1]
                                            ][planetAndPole[0]].release()
            else:
                self.nuke(planetAndPole)

    ####################################################
    #                   ATENÇÃO                        #
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################

    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            # Marte tem uma distância aproximada de dois anos do planeta Terra.
            sleep(2)
        else:
            # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.
            sleep(5)

    def do_we_have_a_problem(self):
        if (random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False

    def general_failure(self):
        print(f"⚡ - [GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")

    def meteor_collision(self):
        print(f"☄️ - [METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfully_launch(self, base):
        if random() <= 0.1:
            print(
                f"❌ - [LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True

    def damage(self):
        return random()

    def launch(self, base, planet):
        if(self.successfully_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)
