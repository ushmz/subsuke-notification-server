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
        



'''
そういえば今回春プレ行きますかい？きっぷどうしようか考えてまして．
'''