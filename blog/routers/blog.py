from fastapi import APIRouter
from fastapi import Depends, status
from .. import schemas, database, oauth2
from ..repository import blog_repository
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.create(request, db)


@router.get('/', response_model=List[schemas.BlogResponse])
def get_all_blogs(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.get_all(db)


@router.get('/{blog_id}', response_model=schemas.BlogResponse)
def get_blog_by_id(blog_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.get_by_id(blog_id, db)


@router.delete('/{blog_id}')
def delete_blog(blog_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.delete_by_id(blog_id, db)


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.BlogResponse)
def update_blog(blog_id: int, request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_repository.update_by_id(blog_id, request, db)
