from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# Conectare la MongoDB (port default 27017)
client = MongoClient("mongodb://mongo-users:27017/")
db = client["user_db"]
users_collection = db["users"]

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    users_collection.insert_one(user.dict())
    return {"message": "User registered"}

@app.post("/login")
def login(user: User):
    found = users_collection.find_one({"username": user.username, "password": user.password})
    if not found:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": str(found["_id"])}
