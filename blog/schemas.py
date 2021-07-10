from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str


class BlogSimpleResponse(Blog):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    name: str
    email: str
    blogs: List[BlogSimpleResponse] = []

    class Config:
        orm_mode = True


class BlogResponse(BaseModel):
    title: str
    body: str
    creator: UserResponse

    class Config:
        orm_mode = True
