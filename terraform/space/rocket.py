from random import randrange, random
from time import sleep
import globals


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

    def nuke(self, planet):  # Permitida a alteração
        terraformMutex = globals.get_planets_ref()[
            planet.name]["terraformMutex"]

        print(
            f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
        print(
            f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")

        while planet.terraform > 0:
            terraformMutex.acquire()
            planet.nuke_detected(self.damage(), terraformMutex)

    def voyage(self, planet):  # Permitida a alteração (com ressalvas)
        if self.name == "LION":
            # Nesse caso, o planeta é a base lunar
            moonBase = planet

            # 4 dias de viagem
            sleep(0.011)
            self.do_we_have_a_problem()

            # Precisa de proteção?
            moonBase.uranium += self.uranium
            moonBase.fuel += self.fuel
        else:
            # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
            # Você pode inserir código antes ou depois dela e deve
            # usar essa função.
            self.simulation_time_voyage(planet)
            failure = self.do_we_have_a_problem()
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
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")

    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfully_launch(self, base):
        if random() <= 0.1:
            print(
                f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True

    def damage(self):
        return random()

    def launch(self, base, planet):
        if(self.successfully_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)
