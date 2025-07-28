from fastapi import FastAPI
import json
app = FastAPI()
def load_data():
    with open("patient.json","r") as f:
       data=json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Patient management system"}

@app.get("/about")
def about():
    return {"message": "A fuuly functioned api for patient managememt ."}

@app.get("/view")
def about():
    data=load_data()
    return data

