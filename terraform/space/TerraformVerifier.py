from typing import Callable
from Synchronization.TerraformSync import TerraformSync


def TerraformVerifier(callback: Callable, args):
    """Recebe uma função e seus args a ser chamada quando terminar"""
    semTerraformReady = TerraformSync().semTerraformReady
    # Espera 4 vezes esse semáforo, cada planeta ao estar pronto irá liberar 1 vez esse semáforo
    semTerraformReady.acquire()
    print('-' * 50 + "1")
    semTerraformReady.acquire()
    print('-' * 50 + "2")
    semTerraformReady.acquire()
    print('-' * 50 + "3")
    semTerraformReady.acquire()
    print('-' * 50 + "4")

    # Nesse ponto todos os planetas já tiveram o processo de terraform finalizado
    callback(args)
