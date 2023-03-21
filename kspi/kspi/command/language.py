from kspi.command.model import RequestedOperation, RequestedProvider



def operation(op_fn):

    def wrapper(*modifiers, **kwargs):

        reqOp = RequestedOperation(
            op_fn=op_fn,
            unrealized_kwargs=kwargs
        )

        return reqOp

    return wrapper


def provider(provider_fn):
    def wrapper(**kwargs):

        reqOp = RequestedProvider(
            provider_fn=provider_fn,
            unrealized_kwargs=kwargs
        )

        return reqOp

    return wrapper


def sequence(*ops):
    def yield_ops(ctx):
        for op in ops:
            yield op

    return RequestedOperation(
        op_fn=yield_ops,
        unrealized_kwargs={}
    )