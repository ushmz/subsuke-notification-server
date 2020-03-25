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
            year, month, date = updated.split('-')
            service.sendPushNotfication(task['token'], task['message'], {'year': year, 'month': month, 'date': date, 'updated': updated})
        service.sendPushNotfication('ExponentPushToken[82xhCLLedlQGQwQDTb8rsX]', 'Success.')

