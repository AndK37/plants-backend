from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from auth import AuthHandler



router = APIRouter(prefix='/favorites', tags=['Favorites'])

auth_handler = AuthHandler()



@router.get('/', response_model=List[pyd.PlantSchema])
def get_all_favorites(db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    
    favorites = db.query(models.Favorite).filter(models.Favorite.user_id == user_db.id).all()
    favorite_plants = []
    for fav in favorites:
        favorite_plants.append(db.query(models.Plant).filter(models.Plant.id == fav.plant_id).first())
    return favorite_plants

@router.post('/')
def add_favorite(plant_id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    
    favorite_db = db.query(models.Favorite).filter(models.Favorite.user_id == user_db.id).all()
    for fav in favorite_db:
        if fav.plant_id == plant_id:
            db.delete(fav)
            db.commit()

            return {'msg': f'{db.query(models.Plant).filter(models.Plant.id == plant_id).first().name} removed from favorite'}
    favorite_db = models.Favorite()
    favorite_db.user_id = user_db.id
    favorite_db.plant_id = plant_id

    db.add(favorite_db)
    db.commit()

    return {'msg': f'{db.query(models.Plant).filter(models.Plant.id == plant_id).first().name} added to favorite'}
