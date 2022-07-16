import sys
import threading
from typing import Callable
from Synchronization.TerraformSync import TerraformSync


def TerraformVerifier(callback: Callable, args):
    """Recebe uma função e seus args a ser chamada quando terminar"""
    semTerraformReady = TerraformSync().semTerraformReady
    # Espera 4 vezes esse semáforo, cada planeta ao estar pronto irá liberar 1 vez esse semáforo
    semTerraformReady.acquire()
    semTerraformReady.acquire()
    semTerraformReady.acquire()
    semTerraformReady.acquire()

    # Nesse ponto todos os planetas já tiveram o processo de terraform finalizado, então o callback é chamado
    # Nesse caso específico esse callback irá setar uma flag global como True, finalizando as threads
    callback(args)

    print('All planets are now terraformed, the Project Endurance was successfully completed!')
    print(threading.active_count())
    sys.exit()
