from threading import Thread
from time import sleep
from Synchronization.MinesSync import MinesSync
import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class Pipeline(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_pipeline(self):
        print(
            f"🔨 - [{self.location}] - {self.unities} oil unities are produced."
        )

    def produce(self):
        MinesSync().fuelMineMutex.acquire()
        if (self.unities < self.constraint):
            self.unities += 17
            self.print_pipeline()
        MinesSync().fuelMineMutex.release()
        sleep(0.001)

    def run(self):
        globals.acquire_print()
        self.print_pipeline()
        globals.release_print()

        while (globals.get_release_system() == False):
            pass

        while not globals.getTerraformReady():
            self.produce()
