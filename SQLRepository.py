import configparser
import os
import psycopg2 as psql
from psycopg2.extras import DictCursor # Not Working?

class SQLRepository:

    def getConnecton(self):
        '''
        This is for local.
        parser = configparser.ConfigParser()
        parser.read("./psql.ini")
        connection = psql.connect(
            host=parser["sql"]["host"],
            port=parser["sql"]["port"],
            user=parser["sql"]["user"],
            password=parser["sql"]["password"],
            database=parser["sql"]["database"]
        )
        '''
        dbn = os.environ.get('DATABASE_URL')
        connection = psql.connect(dbn)
        return connection
    
    def registorUserToken(self, token, name=None):
        # with self.getConnecton as connection:
        connection = self.getConnecton()
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            if name:
                cursor.execute(f"insert into users(token, name) values('{token}', '{name}');")
            else:
                cursor.execute(f"insert into users(token) values('{token}');")
        except Exception as e:
            print(e)
        else:
            connection.commit()
        finally:
            cursor.close()
            connection.close()
        
    def schedulePushNotification(self, token, message, cycle, date):
        # with self.getConnecton as connection:
        
        connection = self.getConnecton()
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(f"insert into pending(token, message, cycle, next) values('{token}', '{message}', '{cycle}', '{date}');")
        except Exception as e:
            print(e)
        else:
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def collectAllonSchedule(self):
        # with self.getConnecton as connection:
        connection = self.getConnecton()        
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            # TODO 評価式
            cursor.execute(f'select * from pending where next = current_date;')
            result = cursor.fetchall()
            disc = cursor.description
            rs = []
            for r in result:
                column = {}
                for k, v in zip(disc, r):
                    column[k.name] = v
                rs.append(column)
            print(rs)
        except Exception as e:
            print(e)
        else:
            return result
        finally:
            cursor.close()
            connection.close()
    
    def updateSchedule(self, pendingId, date):
        # with self.getConnecton as connection:
        connection = self.getConnecton()
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(f'select cycle from pending where pending_id = {pendingId}')
            cycle = cursor.fetchone[0]
            if cycle == '月':
                cursor.execute(f"update pending set date = date + interval '1 month' where pending_id = {pendingId};")

        except TypeError as te:
            print(te)
        else:
            connection.commit()
        finally:
            cursor.close()
            connection.close()
    

