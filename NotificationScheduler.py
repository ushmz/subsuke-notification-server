import datetime
import multiprocessing
import schedule
import time
from threading import Lock

from Service import Service
from SQLRepository import SQLRepository

class NotificationScheduler:
    
    def execute(self):
        sql = SQLRepository()
        tasks = sql.collectAllonSchedule()
        service = Service()
        for task in tasks:
            sql.updateSchedule(task['token'], task['pending_id'])
            updated = sql.getNextNotificationDate(task['token'], task['pending_id'])
            year = updated.year
            month = updated.month
            date = updated.day
            service.sendPushNotfication(task['token'], task['message'], {'year': int(year), 'month': int(month), 'date': int(date), 'rowid': task['pending_id']})
