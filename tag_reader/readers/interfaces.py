class IBaseTemplate:
    def __init__(self):
        pass

    def getTagGroup(self):
        pass

    def readParameterByName(self, str_name):
        pass

    def is_loaded(self):
        pass

    def toJson(self):
        pass

    def onInstanceLoad(self, instance):
        pass

    def AddSubForOnInstanceLoad(self, objMethod):
        pass

    def RemoveSubOnInstanceLoad(self, objMethod):
        pass