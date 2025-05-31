from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from auth import AuthHandler



router = APIRouter(prefix='/admin', tags=['Admin'])
auth_handler = AuthHandler()



@router.put('/roles/')
def promote(user_id: int, role_id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1:
        raise HTTPException(403)
    
    moderator = db.query(models.User).filter(models.User.id == user_id).first()
    moderator.role_id == role_id

    db.commit()

    return

@router.delete('/reviews/')
def remove_review(review_id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    db.delete(review)
    db.commit()

    return

@router.delete('/users/')
def remove_user(user_id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()

    return

@router.delete('/plants/')
def remove_plant(plant_id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    db.delete(plant)
    db.commit()

    return