import datetime
import multiprocessing
import schedule
import time
from threading import Lock

from Service import Service
from SQLRepository import SQLRepositotry as sql

class NotificationScheduler:

    _instance = None
    _lock = Lock()

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via constractor.')

    @classmethod
    def __internal_new__(cls):
        inst = super.__init__(cls)
        return inst

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls.__internal_new__()
        return cls._instance
    
    def execute(self):
        tasks = sql.collectAllonSchedule()
        for task in tasks:
            Service.sendPushNotfication(task[0], task[1])

            ####### ReMake this as method #######
            if task[2] == '週':
                nextDate = task[3] + datetime.timedelta(weeks=1)
            elif task[2] == '月':
                nextDate = task[3] #+ i month(re-generate datetime object)
            elif task[2] == '年':
                nextDate = task[3] #+ i year(re-generate datetime object)
            ################################
            sql.updateSchedule(task[0], nextDate)
