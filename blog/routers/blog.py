from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get('/', response_model=List[schemas.BlogResponse])
def get_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/{blog_id}', response_model=schemas.BlogResponse)
def get_blog_by_id(blog_id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    return blog


@router.delete('/{blog_id}')
def delete_blog(blog_id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    blog.delete(synchronize_session=False)
    db.commit()


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog with id {id} was not found.')

    blog.update(request, synchronize_session=False)
    db.commit()