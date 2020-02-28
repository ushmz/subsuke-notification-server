import configparser
import mysql.connector as sql

class SQLRepositotry:

    def __init__(self):
        super().__init__()
        _parser = configparser.ConfigParser()
        _parser.read("./mysql.ini")
        self.connection = sql.connect(
            host=_parser["sql"]["host"],
            port=_parser["sql"]["port"],
            user=_parser["sql"]["user"],
            password=_parser["sql"]["password"],
            database=_parser["sql"]["database"]
        )
    
    def registorUserToken(self, token, name=None):
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            if name:
                cursor.execute(f"insert into users(token, name) values('{token}', '{name}');")
            else:
                cursor.execute(f"insert into users(token) values('{token}');")
        except Exception as e:
            print(e)
            self.connection.rollback()
        else:
            self.connection.commit()
        finally:
            cursor.close()
            self.connection.close()
        
    def schedulePushNotification(self, token, message, cycle, date):
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"insert into pending values('{token}', '{message}', '{cycle}', '{date}');")
        except Exception as e:
            print(e)
            self.connection.rollback()
        else:
            self.connection.commit()
        finally:
            cursor.close()
            self.connection.close()

    def collectAllonSchedule(self):
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            # TODO 評価式
            cursor.execute(f'select * from pending where date = ')
            result = cursor.fetchall()
        except Exception as e:
            print(e)
            self.connection.rollback()
        else:
            return result
        finally:
            cursor.close()
            self.connection.close()
    
    def updateSchedule(self, token, date):
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"update pending set date = {date} where token = {token}";)
        except Exception as e:
            print(e)
            self.connection.rollback()
        finally:
            cursor.close()
            self.connection.close()