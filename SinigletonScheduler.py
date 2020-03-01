import datetime
import multiprocessing
import schedule
import time
from threading import Lock

from NotificationScheduler import NotificationScheduler
from Service import Service
from SQLRepository import SQLRepository as sql

class SingletonScheduler(NotificationScheduler):

    _instance = None
    _lock = Lock()

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via constractor.')

    @classmethod
    def __internal_new__(cls):
        inst = super().__init__(cls)
        return inst

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls.__internal_new__()
        return cls._instance
