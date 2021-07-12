from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from blog import models, schemas


def get_all(db: Session):
    return db.query(models.Blog).all()


def create(blog: schemas.Blog, db: Session):
    new_blog = models.Blog(title=blog.title, body=blog.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def get_by_id(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    return blog


def delete_by_id(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    blog.delete(synchronize_session=False)
    db.commit()

    return {'message': 'Deleted'}


def update_by_id(blog_id: int, blog_request: schemas.Blog, db: Session):
    # to fix
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    blog.update(blog_request)
    db.commit()

    return blog
