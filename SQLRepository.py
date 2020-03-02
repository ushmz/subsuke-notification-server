import configparser
import os
import psycopg2 as psql
from psycopg2.extras import DictCursor # Not Working?

class SQLRepository:

    def getConnecton(self):
        '''
        データベースとのコネクションを取得する．

        This is for local.
        '''
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
        '''
        return connection
    
    def registorUserToken(self, token, name=None):
        '''
        プッシュ通知トークンをDBに保存するメソッド．

        Args:
            token(str)  : Expoプッシュトークン
            name(str)   : ユーザーネーム(optional)
        '''
        # with self.getConnecton as connection:
        connection = self.getConnecton()
        cursor = connection.cursor()
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
        '''
        プッシュ通知をDBに保存するメソッド．

        Args:
            token(str)      : Expoプッシュトークン
            message(str)    : 通知本文
            cycle(str)      : 支払い周期[年|月|週]
            date(str)       : 次回通知予定日(yyyy-mm-dd)
        '''
        # with self.getConnecton as connection:
        connection = self.getConnecton()
        cursor = connection.cursor()
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
        '''
        一日一回，その日に送信する通知を返却する．

        Returns:
            result(list)    : 送信する通知情報のオブジェクトのリスト
        
            通知情報オブジェクト構造
            {
                pending_id(int): ID,
                token(str): プッシュトークン,
                message(str): 通知本文,
                cycle(str): 支払いサイクル[年|月|週],
                next: 通知予定日(yyyy-mm-dd)
            }
        '''
        # with self.getConnecton as connection:
        connection = self.getConnecton()        
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            # TODO 評価式
            cursor.execute(f'select * from pending where next = current_date;')
            results = cursor.fetchall()
            
            rs = []
            for result in results:
                rs.append(dict(result))
        except Exception as e:
            print(e)
        else:
            return rs
        finally:
            cursor.close()
            connection.close()


    @DeprecationWarning
    def UNUSE_collectAllonSchedule(self):
        '''
        結果を辞書形式で取得できないため非推奨
        一日一回，その日に送信する通知を返却する．

        Returns:
            result(list)    : 送信する通知情報のオブジェクトのリスト
        
            通知情報オブジェクト構造
            {
                pending_id(int): ID,
                token(str): プッシュトークン,
                message(str): 通知本文,
                cycle(str): 支払いサイクル[年|月|週],
                next: 通知予定日(yyyy-mm-dd)
            }
        '''
        # with self.getConnecton as connection:
        connection = self.getConnecton()        
        cursor = connection.cursor()
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
    
    def updateSchedule(self, pendingId):
        '''
        支払い周期に応じて次回通知日を更新する．
        
        Args:
            pendingId(int)  : ID
        '''
        # with self.getConnecton as connection:
        connection = self.getConnecton()
        cursor = connection.cursor()
        try:
            cursor.execute(f'select cycle from pending where pending_id = {pendingId}')
            cycle = cursor.fetchone()[0]
            print(cycle)
            if cycle == '週':
                cursor.execute(f"update pending set next = next + interval '1 week' where pending_id = {pendingId};")
            elif cycle == '月':
                cursor.execute(f"update pending set next = next + interval '1 month' where pending_id = {pendingId};")
            elif cycle == '年':
                cursor.execute(f"update pending set next = next + interval '1 year' where pending_id = {pendingId};")
        except TypeError as te:
            print(te)
        else:
            connection.commit()
        finally:
            cursor.close()
            connection.close()
    

