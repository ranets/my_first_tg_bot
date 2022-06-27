import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

connection = create_connection("C:\\Users\\ranets2\\Desktop\\projects\\tg_bot\\users.sqlite")


create_users_table = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  password TEXT NOT NULL
);
"""

create_querycount_table = """
CREATE TABLE IF NOT EXISTS querycount(
  user_id INTEGER PRIMARY KEY,
  count INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

create_topquery_table = """
CREATE TABLE IF NOT EXISTS topquery(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  query TEXT NOT NULL,
  count INTEGER NOT NULL
);
"""

execute_query(connection, create_users_table)
execute_query(connection, create_querycount_table)
execute_query(connection, create_topquery_table)  


create_topquery = """
INSERT INTO
  topquery (query, count)
VALUES""" + """
    ('Рис', 1);
"""

#execute_query(connection, create_topquery) 

select_topquery = "SELECT count from topquery"
querys = execute_read_query(connection, select_topquery)

i=[]
for selects in querys:
    i.append(int(str(selects)[1:-2]))
print(i)

string = str(i)
#print((string[1:-2]))

one = (string[1:-2])
print(one)

rice = str('Рис')
#print(rice)
select_select_topquery_2 = "SELECT count FROM topquery WHERE query = " + "'" + rice + "'"

querys_2 = execute_read_query(connection, select_select_topquery_2)

for selects in querys_2:
    print(selects)

update_select_topquery_2 = """
UPDATE
  topquery
SET
  count = 2
WHERE
  count = 1
"""

# execute_query(connection, update_select_topquery_2)