
from database.db import base
from sqlalchemy import Column , String , Integer , ForeignKey
from app.User.model import UserData


class JobData(base):
    __tablename__ = 'jobs'
    job_id = Column(String , primary_key = True)
    job_name = Column(String)
    user_name = Column(String)
