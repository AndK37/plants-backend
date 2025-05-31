from fastapi import FastAPI, Depends,HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from routers import *



app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(plants_router)
app.include_router(roles_router)
app.include_router(categories_router)
app.include_router(favorites_router)
app.include_router(carts_router)
app.include_router(reviews_router)
app.include_router(plants_ratings_router)
app.include_router(orders_router)
app.include_router(admin_router)