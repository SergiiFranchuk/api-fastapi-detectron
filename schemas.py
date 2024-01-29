from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
