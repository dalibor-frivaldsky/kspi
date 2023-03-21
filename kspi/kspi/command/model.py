from kspi.command.context import CommandContext
from typing import Any, Callable



class RequestedOperation:
    
    def __init__(self, op_fn: Callable, unrealized_kwargs: dict):
        self.op_fn = op_fn
        self.unrealized_kwargs = unrealized_kwargs


class RequestedProvider:
    def __init__(self, provider_fn: Callable, unrealized_kwargs: dict):
        self.provider_fn = provider_fn
        self.unrealized_kwargs = unrealized_kwargs