from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models
from typing import List
import pyd
from auth import AuthHandler



router = APIRouter(prefix='/reviews', tags=['Reviews'])

auth_handler = AuthHandler()



@router.post('/', response_model=pyd.ReviewSchema)
def add_review(review: pyd.CreateReview, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    review_db = models.Review()

    review_db.user_id = user_db.id
    review_db.plant_id = review.plant_id
    review_db.review = review.review
    

    db.add(review_db)
    db.commit()

    review_db.upvotes = db.query(models.ReviewRating).filter(models.ReviewRating.review_id == review_db.id).count()
    return review_db

@router.get('/', response_model=List[pyd.ReviewSchema])
def get_all_plant_reviews(id: int, db: Session=Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.plant_id == id).all()
    for review in reviews:
        review.upvotes = db.query(models.ReviewRating).filter(models.ReviewRating.review_id == review.id).count()
    return reviews

@router.post('/like')
def add_review(id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)

    rr_db = db.query(models.ReviewRating).filter(models.ReviewRating.review_id == id, models.ReviewRating.user_id == user_db.id).first()
    if rr_db:
        db.delete(rr_db)
        db.commit()
        return
        
    rr_db = models.ReviewRating()
    rr_db.review_id = id
    rr_db.user_id = user_db.id
    rr_db.upvoted = True
    db.add(rr_db)
    db.commit()
    return

@router.delete('/')
def delete_review(id: int, db: Session=Depends(get_db), jwt=Depends(auth_handler.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.login == jwt).first()
    if not user_db:
        raise HTTPException(401)
    
    r = db.query(models.Review).filter(models.Review.user_id == user_db.id, models.Review.id == id).first()
    if r:
        db.delete(r)
        db.commit()
        return
    else:
        raise HTTPException(404)