from abc import ABC


class AbstractMine(ABC):
    """
    Classe para representar a abstração de uma classe de Mina de recursos

    Não está sendo utilizada, mas serve como base para referências durante desenvolvimento
    """
    @property
    def unities(self) -> int:
        pass

    @property
    def constraints(self) -> int:
        pass
