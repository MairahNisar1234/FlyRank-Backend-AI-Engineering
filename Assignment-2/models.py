from typing import Optional 
from sqlmodel import SQLModel, Field
from pydantic import BaseModel



class Task (SQLModel, table=True):
    id: Optional[int] = Field (default=None, primary_key=True)
    title :str 
    done : bool = False


class TaskUpdate(BaseModel):
    title:str
    done:bool

class TaskCreate(BaseModel):
    title:str