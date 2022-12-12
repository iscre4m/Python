import mysql.connector

connection_config = {
        "host":       "localhost",
        "port":              3306,
    "database": "python_database",
        "user":  "python_db_user",
    "password":             "123"
}

def show_databases(cursor):
    sql = "SHOW DATABASES"
    cursor.execute(sql)
    print(cursor.column_names)
    for row in cursor:
        print(row)


def main():
    try:
        connection = mysql.connector.connect(**connection_config)
    except mysql.connector.Error as error:
        print(f"Failed to connect: {error}")
    else:
        print("Connected")
    cursor = connection.cursor()
    show_databases(cursor)


if __name__ == "__main__":
    main()

