from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from auth import AuthHandler



router = APIRouter(prefix='/categories', tags=['Categories'])

auth_handler = AuthHandler()



@router.get('/', response_model=List[pyd.BaseCategory])
def get_all_categories(db: Session=Depends(get_db)):
    categories = db.query(models.Category).all()

    if not categories:
        raise HTTPException(404, "Категории не найдены")

    return categories


@router.get('/{id}', response_model=pyd.BaseCategory)
def get_category_by_id(id: int, db: Session=Depends(get_db)):
    categoriy = db.query(models.Category).filter(models.Category.id == id).first()

    if not categoriy:
        raise HTTPException(404, "Категория не найдена")

    return categoriy


@router.post('/', response_model=pyd.BaseCategory)
def create_category(category: pyd.CreateCategory, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    category_db = models.Category()
    category_db.name = category.name

    db.add(category_db)
    db.commit()

    return category_db


@router.put('/{id}', response_model=pyd.BaseCategory)
def update_category(id: int, category: pyd.CreateCategory, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    category_db = db.query(models.Category).filter(models.Category.id == id).first()
    if not category_db:
        raise HTTPException(404, "Категория не найдена")

    category_db.name = category.name

    db.commit()

    return category_db


@router.delete('/{id}')
def delete_category(id: int, category: pyd.CreateCategory, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    category_db = db.query(models.Category).filter(models.Category.id == id).first()
    if not category_db:
        raise HTTPException(404, "Категория не найдена")
    
    db.delete(category_db)
    db.commit()

    return {'msg': 'Удалено'}