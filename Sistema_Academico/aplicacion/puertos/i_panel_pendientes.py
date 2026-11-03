from typing import Protocol


class IPanelPendientes(Protocol):
    def consultar(self): ...
