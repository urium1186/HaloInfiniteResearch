class Chunk:
    def __init__(self, p_path='', p_len=0, p_data=b''):
        self.path = p_path
        self.len = p_len
        self.data = p_data


class RegionData:
    def __init__(self):
        self.region_id = -1
        self.permutation_id = -1
        self.style_id_override = -1


class Event(object):

    def __init__(self):
        self.__eventhandlers = []

    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)
