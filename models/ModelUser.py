from .entities.User import User


class ModelUser:

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT nombre_AS, documento, usuario, password FROM user WHERE documento = '{}'".format(
                user.documento
            )
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(
                    row[0], row[2], User.check_password(row[4], user.password), row[1]
                )
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
