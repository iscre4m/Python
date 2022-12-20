import mysql.connector
import random
import hashlib
import uuid
import time

class User:
    def __init__(self,  row = None):
        if row == None:
            self.id         = None
            self.username   = None
            self.password   = None
            self.name       = None
            self.salt       = None
            self.avatar     = None
            self.email      = None
            self.email_code = None
            self.del_dt     = None
        elif isinstance(row, dict):
            self.id         = row["id"]
            self.username   = row["username"]
            self.password   = row["password"]
            self.name       = row["name"]
            self.salt       = row["salt"]
            self.avatar     = row["avatar"]
            self.email      = row["email"]
            self.email_code = row["email_code"]
            self.del_dt     = row["del_dt"]
        else:
            raise ValueError("row type unsupported")

    def __repr__(self):
        return str(self.__dict__)


class UserDAO:
    def __init__(self, connection: mysql.connector.MySQLConnection):
        self.connection = connection

    def make_salt(self, length = 20):
        return random.randbytes(length).hex()
    
    def hash_password(self, password, salt):
        return hashlib \
            .sha1((password + salt) \
            .encode()) \
            .hexdigest()

    def make_email_code(self):
        return self.make_salt(3)

    def create(self, user: User):
        user.id = str(uuid.uuid4())
        user.salt = self.make_salt()
        user.password = self.hash_password(user.password, user.salt)
        user.email_code = self.make_email_code()
        keys = user.__dict__.keys()
        columns = ','.join(f"`{x}`" for x in keys)
        values = ','.join(f"%({x})s" for x in keys)
        sql = f"INSERT INTO users({columns}) VALUES({values})"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, user.__dict__)
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Create failed: {error}")
        else:
            print("User created")
        finally:
            cursor.close()
    
    def read(self, id = None, username = None, ignore_deleted = True):
        sql = "SELECT u.* FROM `users` AS u"
        params = []
        if id:
            sql += " WHERE u.`id` = %s"
            params.append(id)
        if username:
            sql += " AND" if id else " WHERE"
            sql += " u.`username` = %s"
            params.append(username)
        if ignore_deleted:
            sql += (" AND" if id or username else " WHERE") + \
            " u.`del_dt` IS NULL"
        try:
            cursor = self.connection.cursor(dictionary = True)
            cursor.execute(sql, params)
        except mysql.connector.Error as error:
            print(f"Read failed: {error}")
        else:
            return tuple(User(row) for row in cursor)
        finally:
            cursor.close()

    def read_by_credentials(self, username, password):
        user = (self.read(username = username) + (None,))[0]
        if (user and self.hash_password(password, user.salt) == user.password):
            return user
        return None
    
    def update(self, user: User):
        sql = "UPDATE `users` u SET "
        data_to_edit = dict()
        data_to_edit["id"] = user.id
        for k, v in user.__dict__.items():
            if v == None:
                continue
            data_to_edit[k] = v
        sql += ",".join(f"u.`{k}` = %({k})s" for k in data_to_edit.keys())
        sql += f" WHERE u.`id` = %(id)s"
        try:
            cursor = self.connection.cursor(dictionary = True)
            cursor.execute(sql, data_to_edit)
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Update failed: {error}")
        else:
            print("User updated")
        finally:
            cursor.close()
    
    def delete(self, user: User):
        sql = '''
            UPDATE `users` AS u 
            SET u.`del_dt` = %s 
            WHERE u.`id` = %s
        '''
        try:
            cursor = self.connection.cursor()
            user.del_dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            cursor.execute(sql, [user.del_dt, user.id])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Delete failed: {error}")
        else:
            print("User deleted")
            return True
        finally:
            cursor.close()
        return False

    def restore(self, user: User):
        sql = '''
            UPDATE `users` AS u 
            SET u.`del_dt` = NULL 
            WHERE u.`id` = %s
        '''
        try:
            cursor = self.connection.cursor()
            user.del_dt = None
            cursor.execute(sql, [user.id])
            self.connection.commit()
        except mysql.connector.Error as error:
            print(f"Restore failed: {error}")
        else:
            print("User restored")
        finally:
            cursor.close()

    def is_username_free(self, username):
        sql = '''
            SELECT COUNT(*) FROM `users` AS u 
            WHERE u.`username` = %s
        '''
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, [username])
            return True if cursor.fetchone()[0] == 0 else False
        except mysql.connector.Error as error:
            print(f"Read error: {error}")
        finally:
            cursor.close()