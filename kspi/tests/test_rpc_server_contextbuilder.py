from kspi.rpc.server import ContextBuilder


def test_register_and_build():
    ctx_builder = ContextBuilder()
    ctx_builder.register_builder('test', lambda: 10)

    assert ctx_builder.build().test == 10
