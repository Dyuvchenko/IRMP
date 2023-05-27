from sqlalchemy.orm import Session

import ProjectConsts


class DataBaseHelper:
    @staticmethod
    def create_data_base_connection():
        if ProjectConsts.DataBaseEngine:
            return Session(autoflush=False, bind=ProjectConsts.DataBaseEngine)
        else:
            return Exception("База дынных не инициализирована или инициализирована с ошибками")