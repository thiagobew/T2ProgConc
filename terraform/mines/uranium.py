from threading import Thread
from random import randint
from time import sleep
from Synchronization.MinesSync import MinesSync

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class StoreHouse(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_store_house(self):
        print(f"🔨 - [{self.location}] - {self.unities} uranium unities are produced.")

    def produce(self):
        MinesSync().uraniumMineMutex.acquire()
        if (self.unities < self.constraint):
            self.unities += 15
            self.print_store_house()
        MinesSync().uraniumMineMutex.release()
        sleep(0.001)

    def run(self):
        globals.acquire_print()
        self.print_store_house()
        globals.release_print()

        while (globals.get_release_system() == False):
            pass

        while not globals.getTerraformReady():
            self.produce()
