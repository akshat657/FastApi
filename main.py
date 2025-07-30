from fastapi import FastAPI,Path,HTTPException,Query
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