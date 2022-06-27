from pickle import FALSE, TRUE
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
        

def issave(connection, userquery):
    select_topquery = "SELECT query FROM topquery WHERE query = " + "'" + userquery + "'"
    save = execute_read_query(connection, select_topquery)
    #print(save, len(save))
    if len(save) == 0:
        return FALSE
    else:
        #save = save[0]
        return TRUE


def plus_user_query(userquery):
    connection = create_connection("C:\\Users\\ranets2\\Desktop\\projects\\tg_bot\\users.sqlite")

    select_topquery = "SELECT query FROM topquery WHERE query = " + "'" + userquery + "'"
    select_topquerycount = "SELECT count FROM topquery WHERE query = " + "'" + userquery + "'"

    # print(execute_read_query(connection, select_topquery)[0])
    
    if issave(connection, userquery) == TRUE:
        querycount = execute_read_query(connection, select_topquerycount)[0]
        string = str(querycount)
        count = int(string[1:-2])
        update_select_topquery_plus = """
        UPDATE
            topquery
        SET
            count = """ + str(count + 1) + """
        WHERE
            query = """ + "'" + userquery + "'"
        

        execute_query(connection, update_select_topquery_plus)
    else:
        create_topquery = """
        INSERT INTO
            topquery (query, count)
        VALUES
            (""" + "'" + userquery + "'" + """, 1);
        """

        execute_query(connection, create_topquery) 


def show_top():
    connection = create_connection("C:\\Users\\ranets2\\Desktop\\projects\\tg_bot\\users.sqlite")

    select_topquery = "SELECT count from topquery"
    querys = execute_read_query(connection, select_topquery)

    i=[]
    for selects in querys:
        i.append(int(str(selects)[1:-2]))

    tmp=[]
    for k in range(len(i)):
        if k < 10 and max(i) not in tmp:
            tmp.append(max(i))
            i.remove(max(i))
        elif max(i) in tmp:
            i.remove(max(i))
        elif k > 10:
            break
    
    answer = 'Топ популярных запросов:\n'
    for element in tmp:
        select_topquery_2 = "SELECT query FROM topquery WHERE count = " + "'" + str(element) + "'"

        querys_2 = execute_read_query(connection, select_topquery_2)
        for q in querys_2:
            answer = answer + str(q)[2:-3] + ' - ' + str(element) + '\n'

    return answer




