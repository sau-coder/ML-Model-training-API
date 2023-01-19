from fastapi import FastAPI , UploadFile , File , Form
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import List
from uuid import uuid4


class User(BaseModel):
    user_name : str
    is_deleted : bool






  




