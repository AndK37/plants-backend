from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from auth import AuthHandler


router = APIRouter(prefix='/plants/ratings', tags=['PlantsRatings'])

auth_handler = AuthHandler()

@router.post('/')
def rate_plant(plant_id: int, rating: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    pr_db = db.query(models.PlantRating).filter(models.PlantRating.plant_id == plant_id, models.PlantRating.user_id == user_db.id).first()
    if pr_db:
        if rating == 0:
            db.delete(pr_db)
            db.commit()
            return
        
        pr_db.rating = rating
        db.commit()
        return

    pr_db = models.PlantRating()

    pr_db.user_id = user_db.id
    pr_db.plant_id = plant_id
    pr_db.rating = rating

    db.add(pr_db)
    db.commit()

    return

@router.put('/')
def update_plant_rate(plant_id: int, rating: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    pr_db = db.query(models.PlantRating).filter(models.PlantRating.plant_id == plant_id, models.PlantRating.user_id == user_db.id).first()
    pr_db.rating = rating

    db.commit()

    return 

@router.delete('/')
def remove_plant_rate(plant_id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    pr_db = db.query(models.PlantRating).filter(models.PlantRating.plant_id == plant_id, models.PlantRating.user_id == user_db.id).first()

    db.delete(pr_db)
    db.commit()

    return 

