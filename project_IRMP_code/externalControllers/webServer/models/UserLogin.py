from sqlalchemy import Column, Integer, String

from db.DataBaseObject import DataBaseObject


class UserLogin(DataBaseObject):
    __tablename__ = "users"

    login = Column(String, unique=True)

    password = Column(String)

    __is_authenticated = False

    def logout(self):
        self.__is_authenticated = False

    @staticmethod
    def fromDB(user_id, db):
        user_login = db.get(UserLogin, user_id)
        if user_login:
            user_login.__is_authenticated = True
            return user_login
        else:
            return UserLogin()

    @property
    def is_authenticated(self):
        return self.__is_authenticated

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id
        # return str(self.__user["id"])
