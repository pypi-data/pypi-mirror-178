from collections.abc import Mapping
from functools import cached_property
from typing import Callable, Dict, List, Optional, Type

from injector import Injector, Scope
from setuptools.namespaces import flatten

from scuti.domain.cqrs.bus.command_bus import CommandBus
from scuti.domain.cqrs.bus.effect_handler import EffectHandler
from scuti.domain.cqrs.bus.event_bus import EventBus
from scuti.domain.cqrs.bus.query_bus import QueryBus
from scuti.domain.cqrs.bus.state_management.condition import condition_property
from scuti.domain.cqrs.bus.state_management.effect_to_state_mapping import effect_to_state_mapper_property
from scuti.domain.cqrs.effects import Command, Effect, Event, Query
from scuti.domain.model.modules import DomainModule
from scuti.domain.model.repository.repository import Repository
from scuti.infrastructure.domain.cqrs.bus.build_effect_handlers.asynchronous_class import \
    build_asynchronous_class_effect_handler
from scuti.infrastructure.domain.cqrs.bus.build_effect_handlers.asynchronous_state_managing_effect_handler import \
    build_asynchronous_state_managing_class_effect_handler
from scuti.infrastructure.domain.cqrs.bus.build_effect_handlers.synchronous_class import \
    build_synchronous_class_effect_handler
from scuti.infrastructure.domain.cqrs.bus.build_effect_handlers.synchronous_state_managing_effect_handler import \
    build_synchronous_state_managing_class_effect_handler
from scuti.infrastructure.domain.cqrs.cqrs_module import CQRSDomainModule
from scuti.infrastructure.registering.inspection.plum_inspection import InspectionResult, inspect
from scuti.infrastructure.threading.thread import Thread


class DomainApplication:
    def __init__(self,
                 config: Mapping,
                 domains: List[Type[DomainModule]] = None,
                 injector: Optional[Injector] = None):
        domains = domains if domains is not None else []
        self.__application_config = config
        self.__domains: List[Type[DomainModule]] = [CQRSDomainModule] + domains
        self.__domain_instances: Dict[Type[DomainModule], DomainModule] = self.__instantiate_domain_modules()
        self.__injector: Injector = injector if injector is not None else self.__build_injector()
        self.__threads_instances: List[Thread] = []
        self.__register_effect_handlers()

    def start(self):
        self.__threads_instances = self.__start_modules_threads()
        self.__run_module_init_commands()

    def injector(self) -> Injector:
        return self.__injector

    def config(self) -> Mapping:
        return self.__application_config

    def stop(self):
        for thread in self.__threads_instances:
            thread.stop()

        for thread in self.__threads_instances:
            thread.join(timeout=1)

        for thread in self.__threads_instances:
            if thread.is_alive():
                raise RuntimeError(f"Thread: {thread.name} is alive after stop and join. Consider using "
                                   f"self.should_stop() on threads")
        self.__threads_instances = []

    @cached_property
    def command_bus(self) -> CommandBus:
        return self.__injector.get(CommandBus)

    @cached_property
    def event_bus(self) -> EventBus:
        return self.__injector.get(EventBus)

    @cached_property
    def query_bus(self) -> QueryBus:
        return self.__injector.get(QueryBus)

    def __str__(self):
        return f"This is an app running these domains: {', '.join([domain.__name__ for domain in self.__domain_instances.keys()])}"

    def __build_injector(self):
        def build_custom_binder(interface_type: Type, concrete_type: Type, scope: Scope):
            def bind(binder):
                binder.bind(interface_type, concrete_type, scope)

            return bind

        binding_definitions = list(flatten([instance.bindings() for instance in self.__domain_instances.values()]))
        adapted_bindings = [build_custom_binder(*binding) if isinstance(binding, tuple) else binding
                            for binding in binding_definitions]
        injector = Injector(adapted_bindings)
        return injector

    def __instantiate_domain_modules(self) -> Dict[Type[DomainModule], DomainModule]:
        return {module: module(self.__application_config) for module in self.__domains if
                issubclass(module, DomainModule)}

    def __start_modules_threads(self) -> List[Thread]:
        result = []
        all_threads_to_start = list(flatten([module.processes() for module in (self.__domain_instances.values())]))
        for thread_type in all_threads_to_start:
            thread = self.injector().get(thread_type)
            thread.start()
            result += [thread]
        return result

    def __run_module_init_commands(self):
        all_initial_commands = list(flatten([module.init() for module in self.__domain_instances.values()]))
        [self.command_bus.handle(command) for command in all_initial_commands if command is not None]

    def __register_effect_handlers(self):
        effect_handlers_to_inspect = list(
            flatten([module.effect_handlers() for module in self.__domain_instances.values()]))
        if not effect_handlers_to_inspect:
            return
        # TODO externalize builder selection to a config?
        for handler_type in effect_handlers_to_inspect:
            if type(handler_type) is tuple:
                handler_type, repository = handler_type
                async_builder = build_asynchronous_state_managing_class_effect_handler
                sync_builder = build_synchronous_state_managing_class_effect_handler
            else:
                repository = None
                async_builder = build_asynchronous_class_effect_handler
                sync_builder = build_synchronous_class_effect_handler
            self.__register_handlers(async_builder, self.command_bus, Command, handler_type, repository)
            self.__register_handlers(async_builder, self.event_bus, Event, handler_type, repository)
            self.__register_handlers(sync_builder, self.query_bus, Query, handler_type, repository)

    def __register_handlers(self, handler_builder: Callable,
                            bus,
                            base_effect: Type[Effect],
                            handler: Type[EffectHandler],
                            repository: Optional[Type[Repository]]):
        all_handler_parameters = inspect(handler.handle, should_ignore_self=True,
                                         annotations_to_retrieve=[effect_to_state_mapper_property,
                                                                  condition_property]).values()
        # Avoid registering effects more than once for a given effect handler, this can happen when using effect
        # handler state evolution. See "test_effects_can_change_semantics_depending_on_state_type"
        already_registered_effects = []
        for method in all_handler_parameters:
            if repository is None:
                already_registered_effects += self.__register_effect_handler_without_repository(base_effect,
                                                                                                bus,
                                                                                                method,
                                                                                                handler,
                                                                                                handler_builder,
                                                                                                already_registered_effects)
            else:
                already_registered_effects += self.__register_effect_handler_with_repository(base_effect,
                                                                                             bus,
                                                                                             method,
                                                                                             handler,
                                                                                             handler_builder,
                                                                                             repository,
                                                                                             already_registered_effects)

    def __register_effect_handler_without_repository(self, base_effect: Type[Effect],
                                                     bus,
                                                     method: InspectionResult,
                                                     handler: Type[EffectHandler],
                                                     handler_builder: Callable,
                                                     already_registered_effects: List[Effect] = None):
        already_registered_effects = already_registered_effects if already_registered_effects is not None else []
        condition = method.annotations.get(condition_property, None)
        this_run_effects = []
        for effect in method.parameter_types[-1]:
            if base_effect in effect.__mro__ and effect not in already_registered_effects:
                bus.subscribe(effect, handler_builder(handler, condition, self.injector()))
                this_run_effects += [effect]
        return this_run_effects

    def __register_effect_handler_with_repository(self, base_effect: Type[Effect],
                                                  bus,
                                                  method: InspectionResult,
                                                  handler: Type[EffectHandler],
                                                  handler_builder: Callable,
                                                  repository: Type[Repository],
                                                  already_registered_effects: List[Effect] = None):
        already_registered_effects = already_registered_effects if already_registered_effects is not None else []
        this_run_effects = []
        state_mapper = method.annotations.get(effect_to_state_mapper_property, None)
        condition = method.annotations.get(condition_property, None)
        for effect in method.parameter_types[-1]:
            if state_mapper is None and len(method.parameter_types) == 2:
                raise ValueError(
                    f"Trying to register a handler that requires state without a state_mapper: {handler.__name__}.{effect.__name__}")
            if base_effect in effect.__mro__ and effect not in already_registered_effects:
                bus.subscribe(effect,
                              handler_builder(handler, repository, state_mapper, condition, self.injector()))
                this_run_effects += [effect]
        return this_run_effects
