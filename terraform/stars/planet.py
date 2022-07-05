from threading import Thread, Lock
import globals


class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform, name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self, damage, lock):
        self.terraform -= damage
        lock.release()
        print(
            f"[NUKE DETECTION] - The planet {self.name} was bombed by {damage}. {self.terraform}% UNHABITABLE")

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        # Criando mutex para proteger int terraform
        planets = globals.get_planets_ref()
        planets[self.name]["terraformMutex"] = Lock()

        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while (globals.get_release_system() == False):
            pass
