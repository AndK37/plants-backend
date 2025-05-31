from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from auth import AuthHandler

auth_handler = AuthHandler()

router = APIRouter(prefix='/carts', tags=['Carts'])

@router.get('/', response_model=List[pyd.CartSchema])
def get_cart(db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    cart = db.query(models.Cart).filter(models.Cart.user_id == user_db.id).all()
    cart_plants = []
    for item in cart:
        cart_plants.append({'id': item.id, 'plant': db.query(models.Plant).filter(models.Plant.id == item.plant_id).first(), 'amount': item.amount})

    return cart_plants


@router.post('/')
def add_to_cart(plant_id: int, amount: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    cart_db = models.Cart()
    cart_db.user_id = user_db.id
    cart_db.plant_id = plant_id
    cart_db.amount = amount

    db.add(cart_db)
    db.commit()

    return {'msg': f'{db.query(models.Plant).filter(models.Plant.id == plant_id).first().name} added to cart'}

@router.delete('/')
def remove_from_cart(plant_id: int , db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    cart_item = db.query(models.Cart).filter(models.Cart.user_id == user_db.id, models.Cart.plant_id == plant_id).first()
    db.delete(cart_item)
    db.commit()

    return {'msg': f'{db.query(models.Plant).filter(models.Plant.id == plant_id).first().name} removed from cart'}
        