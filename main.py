from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
import os

app = FastAPI()

# 🟢 Conectare la MongoDB Atlas folosind variabila de mediu
try:
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise Exception("MONGO_URI environment variable not set")

    client = MongoClient(mongo_uri)
    db = client["user_db"]
    users_collection = db["users"]

except Exception as e:
    from fastapi import HTTPException
    raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")


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
    found = users_collection.find_one({
        "username": user.username,
        "password": user.password
    })
    if not found:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": str(found["_id"])}
