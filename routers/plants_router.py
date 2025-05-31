from fastapi import APIRouter, HTTPException, Depends, UploadFile, Query, File
from fastapi.responses import FileResponse
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from datetime import datetime
import os
from auth import AuthHandler



router = APIRouter(prefix='/plants', tags=['Plants'])
auth_handler = AuthHandler()



@router.get('/search/', response_model=List[pyd.PlantSchema])
def search_plants(q:str | None =  Query(default=None), db: Session=Depends(get_db)):
    if not q:
        return []
    plants = db.query(models.Plant).filter(models.Plant.name.like(f'%{q}%')).all()

    return plants


@router.get('/', response_model=List[pyd.PlantSchema])
def get_all_plants(category:int | None =  Query(default=None, gt=0), db: Session=Depends(get_db)):
    if category:
        plants = db.query(models.Plant).filter(models.Plant.category_id == category).all()

        if not plants:
            raise HTTPException(404, "Растения не найдено")
        
        for plant in plants:
            plant.rating = compute_rating(plant, db)
        
        return plants

    plants = db.query(models.Plant).all()

    if not plants:
        raise HTTPException(404, "Растения не найдено")
    
    for plant in plants:
        plant.rating = compute_rating(plant, db)

    return plants


@router.get('/{id}', response_model=pyd.PlantSchema)
def get_plant(id: int, db: Session=Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == id).first()

    if not plant:
        raise HTTPException(404)
    
    plant.rating = compute_rating(plant, db)

    return plant



@router.get('/seller/', response_model=List[pyd.PlantSchema])
def get_all_seller_plants(db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    plants = db.query(models.Plant).filter(models.Plant.seller_id == user_db.id).all()

    if not plants:
        raise HTTPException(404)
    
    for plant in plants:
        plant.rating = compute_rating(plant, db)

    return plants


@router.get('/seller/{id}', response_model=pyd.PlantSchema)
def get_all_seller_plants(id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    plant = db.query(models.Plant).filter(models.Plant.seller_id == user_db.id, models.Plant.id == id).first()

    if not plant:
        raise HTTPException(404)
    
    plant.rating = compute_rating(plant, db)

    return plant


@router.get('/{id}/image')
def get_plant_image_by_id(id: int, db: Session=Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == id).first()

    if not plant:
        raise HTTPException(404, "Растение не найдено")
    
    if not plant.image:
        raise HTTPException(404, "Нет изображения")
    
    if os.path.isfile(f'{plant.image}'):
        return FileResponse(f'{plant.image}')
    
    return None



@router.post('/seller/', response_model=pyd.PlantSchema)
def create_plant(plant: pyd.CreatePlant, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    plant_db = models.Plant()
    plant_db.name = plant.name
    plant_db.desc = plant.desc
    plant_db.price = plant.price
    plant_db.packing = plant.packing
    plant_db.category_id = plant.category
    plant_db.seller_id = user_db.id

    # category_db = db.query(models.Category).filter(models.Category.id == plant.category).first()
    # if not category_db:
    #     raise HTTPException(400, 'Неправильная категория')
    # seller_db = db.query(models.User).filter(models.User.id == plant.seller).first()
    # if not seller_db:
    #     raise HTTPException(400, 'Неправильный продавец')

    db.add(plant_db)
    db.commit()

    return plant_db


@router.put('/{id}/image', response_model=pyd.PlantSchema)
def update_plant_image(id: int, file: UploadFile = File(...), db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    allowed_formats = ['image/png', 'image/jpeg']

    if file.content_type not in allowed_formats:
        raise HTTPException(400, 'Неправильный формат')
    
    if file.size > 2097152:
        raise HTTPException(400, 'Файл больше 2mb')
    
    file.filename = str(datetime.now().timestamp()).replace('.', '0')

    file_dir = f"./img/plants/{file.filename}.{file.content_type[6:]}"
    with open(file_dir, "wb+") as file_object:
        file_object.write(file.file.read())

    plant = db.query(models.Plant).filter(models.Plant.id == id, user_db.id).first()

    if not plant:
        raise HTTPException(404, "Растение не найдено")
    
    plant.image = file_dir
    db.commit()

    return plant


@router.put('/seller/{plant_id}', response_model=pyd.PlantSchema)
def update_plant(plant_id: int, plant: pyd.CreatePlant, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    
    plant_db = db.query(models.Plant).filter(models.Plant.id == plant_id, models.Plant.seller_id == user_db.id).first()
    if not plant_db:
        raise HTTPException(404, "Растение не найдено")

    plant_db.name = plant.name
    plant_db.desc = plant.desc
    plant_db.price = plant.price
    plant_db.packing = plant.packing
    plant_db.category_id = plant.category

    db.commit()

    plant_db.rating = compute_rating(plant_db, db)
    
    return plant_db


@router.delete('/seller/{id}')
def delete_plant(id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    plant_db = db.query(models.Plant).filter(models.Plant.id == id, models.Plant.seller_id == user_db.id).first()
    if not plant_db:
        raise HTTPException(404, "Растение не найдено")

    db.delete(plant_db)
    db.commit()

    return {'msg': 'Удалено'}




def compute_rating(plant, db: Session=Depends(get_db)):
    plant_rating_db = db.query(models.PlantRating).filter(models.PlantRating.plant_id == plant.id).all()
    if not plant_rating_db:
        return None
    rating = 0

    for r in plant_rating_db:
        rating += r.rating

    return round(rating / len(plant_rating_db), 2)