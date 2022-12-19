import mysql.connector
import random

def select_dicts(connection, order="U"):
    sql = "SELECT * FROM test AS t ORDER BY " + \
    ("t.str" if order == "G" else "t.ukr")
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except mysql.connector.Error as error:
        print("select_dicts: ", error)
    else:
        names = cursor.column_names
        # row = cursor.fetchone()
        # print(dict(x for x in zip(names, row)))
        return (dict((k, v) for k, v in zip(cursor.column_names, row))
        for row in cursor)
    finally:
        try:
            connection.commit()
            cursor.close()
        except:
            pass


def select_test(connection, order="U"):
    sql = "SELECT * FROM test AS t ORDER BY " + \
    ("t.str" if order == "G" else "t.ukr")
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except mysql.connector.Error as error:
        print("SELECT: ", error)
    else:
        # row = cursor.fetchone()
        # while row:
        #     print(row)
        #     row = cursor.fetchone()
        print(cursor.column_names)
        for row in cursor:
            print(row)
    finally:
        try:
            connection.commit()
            cursor.close()
        except:
            pass


def rand_str():
    alphabet = "АБВГҐДЕЄЖЗИІЇКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    return ''.join(
        random.choice(alphabet) for i in range(random.choice([3, 4, 5]))
    )


def insert_test(connection):
    sql = "INSERT INTO test(num, str, ukr) VALUES (%s, %s, %s)" 
    str = rand_str()
    num = random.randint(1, 20)
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (num, str, str))
    except mysql.connector.Error as error:
        print("INSERT:", error)
    else:
        print("Insert into 'test'")
    finally:
        cursor.close()


def show_databases(cursor):
    sql = "SHOW DATABASES"
    cursor.execute(sql)
    print(cursor.column_names)
    for row in cursor:
        print(row)


def show_tables(cursor):
    sql = "SHOW TABLES"
    cursor.execute(sql)
    print(cursor.column_names)
    for row in cursor:
        print(row)


def create_table(connection):
    sql = '''CREATE TABLE IF NOT EXISTS test (
              `id`    CHAR(36) PRIMARY KEY DEFAULT UUID(),
             `num`         INT                  DEFAULT 0,
             `str` VARCHAR(10)    COLLATE utf8_general_ci,
             `ukr` VARCHAR(10)    COLLATE utf8_unicode_ci
             ) ENGINE = InnoDB, DEFAULT CHARSET = UTF8
        '''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except mysql.connector.Error as error:
        print("CREATE:", error)
    else:
        print("Created table 'test'")
    finally:
        cursor.close()

def main(connection_config):
    try:
        connection = mysql.connector \
            .connect(**connection_config)
    except mysql.connector.Error as error:
        print(f"Failed to connect:\n{error}")
    else:
        print("Connected")
    # create_table(connection)
    # insert_test(connection)
    # select_test(connection)
    for record in select_dicts(connection):
        print(record["num"], record["str"])


if __name__ == "__main__":
    connection_config = {
           "host":          "localhost",
           "port":                 3306,
       "database":    "python_database",
           "user":     "python_db_user",
       "password":                "123",
    "use_unicode":                 True,
        "charset":            "utf8mb4",
      "collation": "utf8mb4_general_ci"
    }
    main(connection_config)

