from random import randrange, random
from time import sleep
from Abstractions.AbstractPlanet import AbstractPlanet
from Synchronization.MoonResourcesSync import MoonSupplySync
from Synchronization.TerraformSync import TerraformSync
from Enum.Enum import Polo, Rockets
from Synchronization.PlanetsSync import PlanetsSync


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
    def nuke(self, planet: AbstractPlanet) -> bool:
        # Adquire o semáforo para ser um dos dois rockets atacando o planeta
        planetName = planet.name.lower()
        TerraformSync().terraformSemaphoreDic[planetName].acquire()

        # Pega um dos polos e dá o acquire no Lock dele para atacar
        pole = self.__getPoleToAttack(planet)

        # Adquire e depois solta o mutex para alterar o terraform do planeta
        TerraformSync().terraformMutexDic[planetName].acquire()
        planet.nukeDetected(self.damage(), pole)
        TerraformSync().terraformMutexDic[planetName].release()

        # Libera o mutex do polo específico que foi atacado
        PlanetsSync().polesMutexDic[pole][planetName].release()
        # Libera para outro foguete atacar o planeta
        TerraformSync().terraformSemaphoreDic[planetName].release()

    def __getPoleToAttack(self, planet: AbstractPlanet) -> Polo:
        # Nesse ponto é uma certeza que um dos polos está disponível
        planetName = planet.name.lower()

        # Tenta adquirir o mutex do polo norte do planeta
        acquired = PlanetsSync().polesMutexDic[Polo.NORTH][planetName].acquire(blocking=False)

        if not acquired:
            acquired = PlanetsSync().polesMutexDic[Polo.SOUTH][planetName].acquire(blocking=False)
            if acquired:
                return Polo.SOUTH
        else:
            return Polo.NORTH

    def voyage(self, planet: AbstractPlanet):  # Permitida a alteração (com ressalvas)
        if self.name == Rockets.LION:
            # Nesse caso, o planeta é a base lunar
            moonBase = planet
            moonSupplyIA = MoonSupplySync()

            # 4 dias de viagem
            sleep(0.011)

            # Caso haja problemas durante a viagem do foguete para a Lua, libera semáforo para
            # outra base poder enviar o foguete Lion no lugar
            if self.do_we_have_a_problem():
                MoonSupplySync().supplierSem.release()
                return

            # Armazena suprimentos no estoque
            moonBase.receiveLionRocket()

            # Notifica departamento de engenharia da Lua que tem novos recursos
            with moonSupplyIA.moonSuppliesMutex:
                moonSupplyIA.resourcesArrived.notify()
        else:
            # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
            # Você pode inserir código antes ou depois dela e deve
            # usar essa função.

            # Se não houve problemas durante a viagem executa o bombardeamento
            if not self.do_we_have_a_problem():
                self.simulation_time_voyage(planet)
                self.nuke(planet)

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
