from configs.config import Config
from events import Event


class Log:
    onPrint = Event()

    def __init__(self):
        pass

    @staticmethod
    def AddSubscribersForOnPrint(objMethod):
        Log.onPrint += objMethod

    @staticmethod
    def RemoveSubscribersOnPrint(objMethod):
        Log.onPrint -= objMethod

    @staticmethod
    def Print(message):
        if Config.VERBOSE:
            print(message)
        Log.onPrint(message)
