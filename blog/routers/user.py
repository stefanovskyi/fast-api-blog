from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from blog import schemas, models, database
from blog.hashing import Hash
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/use',
    tags=['user']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    hashed_password = Hash.bcrypt(request.password)

    new_user = models.User(name=request.name, email=request.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/', response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{user_id}', response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with id {id} was not found.')

    return user
