import pytest

from kspi.rpc.client import Connection
from kspi.rpc.pickling import Pickling



class ClientSideObject:

    def __init__(self, id):
        self._id = id



@pytest.mark.integration
def test_object_round_trip(ksp_connection: Connection):
    # Create connection
    ksp_connection = Connection('localhost', 18811)

    # Register client- and server-side picklers and unpicklers
    # Use common "Object" type tag across client and server
    # Use diferent class for the object on client and server
    def pickleClientSideObject(obj):
        if isinstance(obj, ClientSideObject):
            return ('Object', obj._id)
        else:
            return None
        
    def unpickleClientSideObject(pid):
        type_tag, id = pid
        if type_tag == 'Object':
            return ClientSideObject(id)
        else:
            return None
        
    ksp_connection.pickling.register_pickler_unpickler(pickleClientSideObject, unpickleClientSideObject)


    def setup_server(ctx):
        class ServerSideObject:

            def __init__(self, id):
                self._id = id

        def pickleServerSideObject(obj):
            if isinstance(obj, ServerSideObject):
                return ('Object', obj._id)
            else:
                return None
        
        def unpickleServerSideObject(pid):
            type_tag, id = pid
            if type_tag == 'Object':
                return ServerSideObject(id)
            else:
                return None
            
        ctx.pickling.register_pickler_unpickler(pickleServerSideObject, unpickleServerSideObject)
        ctx.ctx_builder.register_builder('cls', lambda: ServerSideObject)

        
    ksp_connection.rpc(setup_server)

    # Instantiate client-side object
    # Verify on server-side the expected class of the received object, stored in ctx.cls, which should be ServerSideObject
    obj = ClientSideObject('abc')
    def verify_server_side(ctx):
        return {
            'class_ok': isinstance(obj, ctx.cls),
            'id_ok': obj._id == 'abc',
            'obj': obj
        }
    
    result = ksp_connection.rpc(verify_server_side)

    assert result['class_ok'] == True
    assert result['id_ok'] == True
    assert isinstance(result['obj'], ClientSideObject)
    assert result['obj']._id == 'abc'

    # close connection
    ksp_connection.close()



@pytest.mark.integration
def test_connection_states_are_isolated():
    # setup connection 1, with pickling of classes ClientSideObject1 and ServerSideObject1
    conn1 = Connection('localhost', 18811)

    class ClientSideObject1:
        def __init__(self, id):
            self._id = id

    def pickleClientSideObject1(obj):
        if isinstance(obj, ClientSideObject1):
            return ('Object', obj._id)
        else:
            return None
        
    def unpickleClientSideObject1(pid):
        type_tag, id = pid
        if type_tag == 'Object':
            return ClientSideObject1(id)
        else:
            return None
        
    conn1.pickling.register_pickler_unpickler(pickleClientSideObject1, unpickleClientSideObject1)


    def setup_server1(ctx):
        class ServerSideObject1:
            def __init__(self, id):
                self._id = id

        def pickleServerSideObject(obj):
            if isinstance(obj, ServerSideObject1):
                return ('Object', obj._id)
            else:
                return None
        
        def unpickleServerSideObject(pid):
            type_tag, id = pid
            if type_tag == 'Object':
                return ServerSideObject1(id)
            else:
                return None
            
        ctx.pickling.register_pickler_unpickler(pickleServerSideObject, unpickleServerSideObject)
        ctx.ctx_builder.register_builder('cls', lambda: ServerSideObject1)

    conn1.rpc(setup_server1)


    # setup connection 2, with pickling of classes ClientSideObject2 and ServerSideObject2
    conn2 = Connection('localhost', 18811)

    class ClientSideObject2:
        def __init__(self, id):
            self._id = id

    def pickleClientSideObject2(obj):
        if isinstance(obj, ClientSideObject2):
            return ('Object', obj._id)
        else:
            return None
        
    def unpickleClientSideObject2(pid):
        type_tag, id = pid
        if type_tag == 'Object':
            return ClientSideObject2(id)
        else:
            return None
        
    conn2.pickling.register_pickler_unpickler(pickleClientSideObject2, unpickleClientSideObject2)


    def setup_server2(ctx):
        class ServerSideObject2:
            def __init__(self, id):
                self._id = id

        def pickleServerSideObject(obj):
            if isinstance(obj, ServerSideObject2):
                return ('Object', obj._id)
            else:
                return None
        
        def unpickleServerSideObject(pid):
            type_tag, id = pid
            if type_tag == 'Object':
                return ServerSideObject2(id)
            else:
                return None
            
        ctx.pickling.register_pickler_unpickler(pickleServerSideObject, unpickleServerSideObject)
        ctx.ctx_builder.register_builder('cls', lambda: ServerSideObject2)

    conn2.rpc(setup_server2)


    # Instantiate ClientSideObject1
    # Verify on server-side the expected class of the received object, stored in ctx.cls, which should be ServerSideObject1
    obj1 = ClientSideObject1('abc')
    def verify_server_side1(ctx):
        return {
            'class_1_ok': isinstance(obj1, ctx.cls),
            'class_1_name': ctx.cls.__name__,
            'id_1_ok': obj1._id == 'abc',
            'obj1': obj1
        }
    
    result = conn1.rpc(verify_server_side1)

    assert result['class_1_ok'] == True
    assert result['class_1_name'] == 'ServerSideObject1'
    assert result['id_1_ok'] == True
    assert isinstance(result['obj1'], ClientSideObject1)
    assert result['obj1']._id == 'abc'


    # Instantiate ClientSideObject2
    # Verify on server-side the expected class of the received object, stored in ctx.cls, which should be ServerSideObject2
    obj2 = ClientSideObject2('def')
    def verify_server_side2(ctx):
        return {
            'class_2_ok': isinstance(obj2, ctx.cls),
            'class_2_name': ctx.cls.__name__,
            'id_2_ok': obj2._id == 'def',
            'obj2': obj2
        }
    
    result = conn2.rpc(verify_server_side2)

    assert result['class_2_ok'] == True
    assert result['class_2_name'] == 'ServerSideObject2'
    assert result['id_2_ok'] == True
    assert isinstance(result['obj2'], ClientSideObject2)
    assert result['obj2']._id == 'def'


    # close connections
    conn1.close()
    conn2.close()