from sqlalchemy import Integer , String , Boolean , Column , DateTime
from database.db import base
import datetime


class UserData(base):
    __tablename__ = 'user_data'
    user_name = Column(String)
    user_id = Column(String , primary_key = True)
    created_at = Column(DateTime)
    is_deleted = Column(Boolean)
