from .base_models import *
from typing import List



class UserSchema(BaseUser):
    role: BaseRole


class PlantSchema(BasePlant):
    category: BaseCategory
    seller: BaseUser

class FavoriteSchema(BaseFavorite):
    plant: PlantSchema

class CartSchema(BaseCart):
    plant: PlantSchema

class ReviewSchema(BaseReview):
    user: BaseUser
    
class OrderSchema(BaseOrder):
    plant: PlantSchema
    