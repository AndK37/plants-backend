from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from auth import AuthHandler



router = APIRouter(prefix='/orders', tags=['Orders'])
auth_handler = AuthHandler()



@router.get('/' , response_model=List[pyd.OrderSchema])
def get_orders(db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    
    orders_db = db.query(models.Order).filter(models.Order.user_id == user_db.id).all()

    return orders_db


@router.post('/cart')
def convert_cart_to_orders(db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_db.id).all()


    for i in cart:
        order_db = models.Order()
        order_db.user_id = user_db.id
        order_db.plant_id = i.plant_id
        order_db.amount = i.amount
        db.add(order_db)
        db.delete(i)

    db.commit()
