from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class BlogResponse(Blog):

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(User):
    name: str
    email: str

    class Config:
        orm_mode = True
