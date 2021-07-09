from fastapi import FastAPI
from . import schemas

app = FastAPI()


@app.post('/blog')
def create_blog(blog: schemas.Blog):
    return blog
