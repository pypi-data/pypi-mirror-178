from abc import ABC, abstractmethod
from typing import Callable, Type

from scuti.domain.cqrs.bus.hooks.bus_hook import BusHook
from scuti.domain.cqrs.effects import Effect


class AsynchronousBus(ABC):
    @abstractmethod
    def drain(self, block: bool = False):
        pass

    @abstractmethod
    def handles(self, item_type: Type[Effect]) -> bool:
        pass

    @abstractmethod
    def handle(self, item_type: Effect):
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def subscribe(self, item_type: Type[Effect], handler: Callable[[Effect], None], human_friendly_name: str):
        pass

    @abstractmethod
    def register_hook(self, hook: BusHook):
        pass

    @abstractmethod
    def shutdown(self):
        pass
