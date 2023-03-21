import dill as pickle
import io



pickle.settings["recurse"] = True



class _Pickler(pickle.Pickler):

    def __init__(self, file, picklers):
        super().__init__(file)
        self._picklers = picklers


    def persistent_id(self, obj):
        pid = None

        for p in self._picklers:
            pid = p(obj)
            if pid != None:
                break

        return pid
    


class _Unpickler(pickle.Unpickler):

    def __init__(self, file, unpicklers):
        super().__init__(file)
        self._unpicklers = unpicklers


    def persistent_load(self, pid):
        obj = None

        for u in self._unpicklers:
            obj = u(pid)
            if obj != None:
                break

        if obj != None:
            return obj
        else:
            raise pickle.UnpicklingError(f"unsupported persistent object: {pid}")



class Pickling:

    def __init__(self):
        self._picklers = []
        self._unpicklers = []

    
    def register_pickler_unpickler(self, pickler, unpickler):
        self._picklers.append(pickler)
        self._unpicklers.append(unpickler)


    def unregister_all(self):
        self._picklers = []
        self._unpicklers = []


    def build_pickler(self, file):
        return _Pickler(file, self._picklers)
    

    def build_unpickler(self, file):
        return _Unpickler(file, self._unpicklers)
    

    def dumps(self, obj):
        buffer = io.BytesIO()
        self.build_pickler(buffer).dump(obj)
        return buffer.getvalue()


    def loads(self, obj_dump):
        buffer = io.BytesIO(obj_dump)
        return self.build_unpickler(buffer).load()