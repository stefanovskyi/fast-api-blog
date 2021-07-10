from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from .hashing import Hash
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blog'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/blog', response_model=List[schemas.BlogResponse], tags=['blog'])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{blog_id}', response_model=schemas.BlogResponse, tags=['blog'])
def get_blog_by_id(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    return blog


@app.delete('/blog/{blog_id}', tags=['blog'])
def delete_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    blog.delete(synchronize_session=False)
    db.commit()


@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    blog.update(request, synchronize_session=False)
    db.commit()


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse, tags=['user'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)

    new_user = models.User(name=request.name, email=request.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user', response_model=List[schemas.UserResponse], tags=['user'])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{user_id}', response_model=schemas.UserResponse, tags=['user'])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with id {id} was not found.')

    return user

