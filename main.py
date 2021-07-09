from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.get('/')
def index():

    return {'data': {'name': 'alex'}}


class BlogModel(BaseModel):
    name: str
    age: int
    description: Optional[str] = None


@app.post('/blog')
def post_blog(blog: BlogModel):

    return {'data': 'done'}
