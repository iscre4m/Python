import mysql.connector
import random
import hashlib
import uuid

class User:
    def __init__(self,  cursor = None):
        if cursor == None:
            self.id         = None
            self.username   = None
            self.password   = None
            self.name       = None
            self.salt       = None
            self.avatar     = None
            self.email      = None
            self.email_code = None
        else:
            row = cursor.fetchone()
            if not row : raise ValueError("Cursor has no data")
            data = dict((k, v) for k, v in zip(cursor.column_names, row))
            self.id         = data["id"]
            self.username   = data["username"]
            self.password   = data["password"]
            self.name       = data["name"]
            self.salt       = data["salt"]
            self.avatar     = data["avatar"]
            self.email      = data["email"]
            self.email_code = data["email_code"]


class UserDAO:
    def __init__(self, connection: mysql.connector.MySQLConnection):
        self.connection = connection

    def make_salt(self, length = 20):
        return random.randbytes(length).hex()
    
    def hash_password(self, password: str, salt: str):
        return hashlib.sha1((password + salt).encode()).hexdigest()

    def make_email_code(self):
        return self.make_salt(3)

    def create(self, user: User):
        cursor = self.connection.cursor()
        user.id = str(uuid.uuid4())
        user.salt = self.make_salt()
        user.password = self.hash_password(user.password, user.salt)
        user.email_code = self.make_email_code()
        keys = user.__dict__.keys()
        sel = ','.join(f"`{x}`" for x in keys)
        values = ','.join(f"%({x})s" for x in keys)
        sql = f"INSERT INTO users({sel}) VALUES({values})"
        try:
            cursor.execute(sql, user.__dict__)
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Create: {error}")
        else:
            print("User created")
        finally:
            cursor.close()


def main(db_config):
    try:
        connection = mysql.connector \
            .connect(**db_config)
    except mysql.connector.Error as error:
        print(f"Failed to connect:\n{error}")
    else:
        print("Connected")
    
    user = User()
    user.username = "david"
    user.email = "david@gmail.com"
    user.name = "David"
    user.password = "123"

    user_dao = UserDAO(connection)
    user_dao.create(user)


if __name__ == "__main__":
    import configs
    main(configs.DB)