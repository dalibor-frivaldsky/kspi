from kspi.command.language import operation, provider, sequence
from kspi.command.model import RequestedOperation, RequestedProvider



def test_operation_decorator_adheres_to_interface():
    @operation
    def test_operation():
        pass

    op: RequestedOperation = test_operation(kwa1='abc', kwa2='def')

    assert isinstance(op, RequestedOperation)
    assert op.unrealized_kwargs == {
        'kwa1': 'abc',
        'kwa2': 'def'
    }


def test_provider_decorator_adheres_to_interface():
    @provider
    def test_provider():
        pass
    
    p: RequestedProvider = test_provider(kwa1='abc', kwa2='def')

    assert isinstance(p, RequestedProvider)
    assert p.unrealized_kwargs == {
        'kwa1': 'abc',
        'kwa2': 'def'
    }

    try:
        p: RequestedProvider = test_provider('no positional args allowed')
        assert False
    except TypeError:
        pass


def test_sequence_yields_all_requested_operations():
    @operation
    def op1():
        pass

    @operation
    def op2():
        pass

    seq: RequestedOperation = sequence(op1(arg='abc'), op2(arg='def'))

    assert isinstance(seq, RequestedOperation)
    assert seq.unrealized_kwargs == {}

    seq_op_generator = seq.op_fn(ctx=None)
    next_op = next(seq_op_generator)
    assert isinstance(next_op, RequestedOperation)
    assert next_op.unrealized_kwargs == {'arg': 'abc'}

    next_op = next(seq_op_generator)
    assert isinstance(next_op, RequestedOperation)
    assert next_op.unrealized_kwargs == {'arg': 'def'}

    try:
        next(seq_op_generator)
        assert False
    except StopIteration:
        pass