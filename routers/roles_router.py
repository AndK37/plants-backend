from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from auth import AuthHandler



router = APIRouter(prefix='/roles', tags=['Roles'])

auth_handler = AuthHandler()



@router.get('/', response_model=List[pyd.BaseRole])
def get_all_roles(db: Session=Depends(get_db)):
    roles = db.query(models.Role).all()

    if not roles:
        raise HTTPException(404, "Роли не найдены")

    return roles


@router.get('/{id}', response_model=pyd.BaseRole)
def get_role_by_id(id: int, db: Session=Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == id).first()

    if not role:
        raise HTTPException(404, "Роль не найдена")

    return role


@router.post('/', response_model=pyd.BaseRole)
def create_role(role: pyd.CreateRole, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    role_db = models.Role()
    role_db.name = role.name

    db.add(role_db)
    db.commit()

    return role_db


@router.put('/{id}', response_model=pyd.BaseRole)
def update_role(id: int, role: pyd.CreateRole, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    role_db = db.query(models.Role).filter(models.Role.id == id).first()
    if not role_db:
        raise HTTPException(404, "Роль не найдена")

    role_db.name = role.name

    db.commit()

    return role_db


@router.delete('/{id}')
def delete_role(id: int, role: pyd.CreateRole, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    if user_db.role_id != 1 or user_db.role_id != 2:
        raise HTTPException(403)

    role_db = db.query(models.Role).filter(models.Role.id == id).first()
    if not role_db:
        raise HTTPException(404, "Роль не найдена")
    
    db.delete(role_db)
    db.commit()

    return {'msg': 'Удалено'}