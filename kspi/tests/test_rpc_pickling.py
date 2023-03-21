import io
import pytest

from kspi.rpc.pickling import Pickling



class RemoteObjectTest:

    def __init__(self, id):
        self._id = id


@pytest.fixture
def remote_object_pickling():
    state = {'pickled': False, 'unpickled': False}

    def pickleRemoteObjectTest(obj):
        if isinstance(obj, RemoteObjectTest):
            state['pickled'] = True
            return ('RemoteObjectTest', obj._id)
        else:
            return None
        
    def unpickleRemoteObjectTest(pid):
        type_tag, id = pid
        if type_tag == 'RemoteObjectTest':
            state['unpickled'] = True
            return RemoteObjectTest(id)
        else:
            return None
        
    pickling = Pickling()
    pickling.register_pickler_unpickler(pickleRemoteObjectTest, unpickleRemoteObjectTest)

    return [pickling, state]


def test_pickler_building_and_calling(remote_object_pickling):
    pickling, state = remote_object_pickling
    obj = RemoteObjectTest('abcdef')

    buffer = io.BytesIO()
    pickling.build_pickler(buffer).dump(obj)

    assert state['pickled'] == True


def test_unpickler_building_and_calling(remote_object_pickling):
    pickling, state = remote_object_pickling
    obj = RemoteObjectTest('abcdef')

    buffer = io.BytesIO()
    pickling.build_pickler(buffer).dump(obj)
    pickling.build_unpickler(io.BytesIO(buffer.getvalue())).load()

    assert state['unpickled'] == True


def test_dumps_loads_object(remote_object_pickling):
    pickling, state = remote_object_pickling
    obj = RemoteObjectTest('abcdef')

    obj_restored = pickling.loads(pickling.dumps(obj))

    assert obj_restored._id == obj._id
    assert state['pickled'] == True
    assert state['unpickled'] == True


def test_dumps_loads_object_in_fn_closure(remote_object_pickling):
    pickling, state = remote_object_pickling
    obj = RemoteObjectTest('abcdef')

    def return_object_id():
        return obj._id
    
    fn_restored = pickling.loads(pickling.dumps(return_object_id))

    assert return_object_id() == fn_restored()
    assert state['pickled'] == True
    assert state['unpickled'] == True
