from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class BlogResponse(Blog):

    class Config:
        orm_mode = True
