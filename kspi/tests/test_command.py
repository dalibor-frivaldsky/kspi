from types import GeneratorType
from kspi.command.command import Command
from kspi.command.context import CommandContext
from kspi.command.language import operation, provider
from kspi.command.model import RequestedOperation, RequestedProvider



def test_transforming_no_return_requested_operation_adheres_to_interface():
    cmd = Command(ksp=None)
    called = [False]

    @operation
    def no_return_operation():
        called[0] = True
        pass

    op:RequestedOperation = no_return_operation()
    op_as_generator = cmd._requested_operation_to_generator(op, realized_kwargs={})

    assert isinstance(op_as_generator, GeneratorType) == True
    assert called[0] == False
    try:
        next(op_as_generator)
        assert False
    except StopIteration:
        pass
    assert called[0] == True


def test_transforming_returning_requested_operation_adheres_to_interface():
    cmd = Command(ksp=None)
    called = [False]

    @operation
    def returning_operation():
        called[0] = True
        return 'done'

    op:RequestedOperation = returning_operation()
    op_as_generator = cmd._requested_operation_to_generator(op, realized_kwargs={})

    assert isinstance(op_as_generator, GeneratorType) == True
    assert called[0] == False

    result = next(op_as_generator)
    assert called[0] == True
    assert result == 'done'
    try:
        next(op_as_generator)
        assert False
    except StopIteration:
        pass


def test_transforming_yielding_requested_operation_adheres_to_interface():
    cmd = Command(ksp=None)
    called = [False]

    @operation
    def yielding_operation():
        called[0] = True
        yield 'not-done-yet'
        yield 'done'

    op:RequestedOperation = yielding_operation()
    op_as_generator = cmd._requested_operation_to_generator(op, realized_kwargs={})

    assert isinstance(op_as_generator, GeneratorType) == True
    assert called[0] == False

    result = next(op_as_generator)
    assert called[0] == True
    assert result == 'not-done-yet'

    result = next(op_as_generator)
    assert result == 'done'

    try:
        next(op_as_generator)
        assert False
    except StopIteration:
        pass


def test_kwargs_realizing():
    unrealized_kwargs = {
        'strArg': 'abc',
        'intArg': 1,
        'providerArg': RequestedProvider(
            provider_fn=lambda i1, i2, ctx: i1 + i2,
            unrealized_kwargs={
                'i1': 3,
                'i2': RequestedProvider(
                    provider_fn=lambda ctx: 4,
                    unrealized_kwargs={}
                )
            }
        )
    }

    cmd = Command(ksp=None)
    ctx = CommandContext(ksp=None)
    realized_kwargs = cmd._realize_kwargs(ctx=ctx, unrealized_kwargs=unrealized_kwargs)

    assert realized_kwargs == {
        'strArg': 'abc',
        'intArg': 1,
        'providerArg': 7,
        'ctx': ctx
    }


def test_command_execute_one_operation_with_provider():
    @provider
    def double_int_value(i, ctx=None):
        return i*2
    
    result = [0]
    @operation
    def addition_and_multiplication(i1, i2, i3, ctx=None):
        result[0] = i1*i2 + i3

    cmd = Command(ksp=None)
    cmd(
        addition_and_multiplication(
            i1=2,
            i2=3,
            i3=double_int_value(i=5)
        )
    )

    assert result[0] == 16


def test_command_execute_two_operations_in_sequence():
    result = []

    @operation
    def append_number(i, ctx=None):
        result.append(i)

    cmd = Command(ksp=None)
    cmd(
        append_number(i=1),
        append_number(i=2)
    )

    assert result == [1, 2]