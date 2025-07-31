from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
app = FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='Name of the patient',examples=['Akshat'])]
    city:Annotated[str,Field(...,description='city of the patient',examples=['Alwar'])]
    age:Annotated[int,Field(...,gt=0,lt=120,description='age of the patient',examples=['34'])]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient', examples=['male'])]
    height: Annotated[float,Field(...,gt=0,lt=11,description='height of the patient',examples=['4.5'])]
    weight: Annotated[float,Field(...,gt=0,lt=120,description='weight of the patient',examples=['45.9'])]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/self.height**2,2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif 18.5 <= self.bmi < 25:
            return "normal"
        elif 25 <= self.bmi < 30:
            return "overweight"
        else:
            return "obese"
def load_data():
    with open("patient.json","r") as f:
       data=json.load(f)
    return data

def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {"message": "Patient management system"}

@app.get("/about")
def About():
    return {"message": "A fuuly functioned api for patient managememt ."}

@app.get("/view")
def about():
    data=load_data()
    return data
#hello

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str=Path(...,description="This is id of the patient",example="P001")):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,   detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str=Query(...,description="Give the parameter on which you tend to sort[Weight,BMI,Height]"),order:str=Query(default='asc',description='ASC or desc')):
    data=load_data()
    parameter=['weight','height','bmi']
    if sort_by not in parameter:
        raise HTTPException(status_code=400,detail="Invalid parameter selected")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order selected")
    if(order=='desc'):
        sort_order=True
    else:
        sort_order=False
    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)
    return sorted_data


@app.post('/create')
def create_patient(patient:Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail='PAtient already exists')
    data[patient.id]=patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'data created'})
