import configparser
import psycopg2 as psql
from psycopg2.extras import DictCursor

parser = configparser.ConfigParser()
parser.read("../psql.ini")
connection = psql.connect(
    host=parser["sql"]["host"],
    port=parser["sql"]["port"],
    user=parser["sql"]["user"],
    password=parser["sql"]["password"],
    database=parser["sql"]["database"]
)

cursor = connection.cursor(cursor_factory=DictCursor)
cursor.execute('select * from pending')
result = cursor.fetchall()

l = []
for r in result:
    l.append(dict(r))

print(l)