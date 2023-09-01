from pydantic import BaseModel

class GymBookInfo(BaseModel):
    name : str
    email : str
    uid : str | int
    date : int
    time : int