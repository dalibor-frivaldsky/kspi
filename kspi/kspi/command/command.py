from collections import deque
from types import GeneratorType, NoneType
from kspi.command.context import CommandContext
from kspi.command.language import sequence
from kspi.command.model import RequestedOperation, RequestedProvider
from kspi.ksp.ksp import KSP



class Command:

    def __init__(self, ksp: KSP):
        self._ksp = ksp
   

    def __call__(self, *req_ops: RequestedOperation):
        self._execute_requested_op(sequence(*req_ops))

    
    def _execute_requested_op(self, req_op: RequestedOperation):
        ctx = self._prepare_context()
        ops_to_execute = deque()
        ops_to_execute.append(req_op)

        while len(ops_to_execute) > 0:
            op = ops_to_execute.pop()

            if isinstance(op, RequestedOperation):
                realized_kwargs = self._realize_kwargs(ctx, op.unrealized_kwargs)
                op_as_generator = self._requested_operation_to_generator(op, realized_kwargs)

                try:
                    next_op = next(op_as_generator)
                    ops_to_execute.append(op_as_generator)
                    ops_to_execute.append(next_op)
                except StopIteration:
                    pass
            elif isinstance(op, GeneratorType):
                try:
                    next_op = next(op)
                    ops_to_execute.append(op)
                    ops_to_execute.append(next_op)
                except StopIteration:
                    pass
            else:
                raise Exception('Unexpected type of operation to execute')


    def _prepare_context(self) -> CommandContext:
        return CommandContext(
            ksp=self._ksp
        )
    

    def _realize_kwargs(self, ctx: CommandContext, unrealized_kwargs):
        realized_kwargs = {'ctx': ctx}

        for arg_name, arg_value in unrealized_kwargs.items():
            if isinstance(arg_value, RequestedProvider):
                provider: RequestedProvider = arg_value
                provider_realized_kwargs = self._realize_kwargs(ctx, provider.unrealized_kwargs)
                realized_kwargs[arg_name] = provider.provider_fn(**provider_realized_kwargs)
            else:
                realized_kwargs[arg_name] = arg_value

        return realized_kwargs
    

    def _requested_operation_to_generator(self, req_op: RequestedOperation, realized_kwargs: dict) -> GeneratorType:
        def yield_op_results():
            result = req_op.op_fn(**realized_kwargs)

            if isinstance(result, GeneratorType):
                for yielded_result in result:
                    yield yielded_result
            elif isinstance(result, NoneType) == False:
                yield result
            else:
                return

        return yield_op_results()
