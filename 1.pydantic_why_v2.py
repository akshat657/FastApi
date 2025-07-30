from pydantic import BaseModel,AnyUrl,EmailStr,Field
from typing import List, Dict,Optional,Annotated

class Patient(BaseModel):
    #using annonation
    #name:Annonation[str,Field=(max_length=50,title='name of the patient,example=['Nitish','Amit' f])]
    name:str=Field(max_length=50) 
    age:int=Field(gt=0,lt=50)
    weight:float
    married:Optional[bool]=None 
    allergies:List[str]=Field(max_length=4)
    contact:dict[str,str]

patient_info={'name':'Akshat','age':21,'weight':56.7,'married':True,'allergies':['asthma','AIDS'],'contact':{'email':'Asdfgh@gmail.com'}}
Patient1=Patient(**patient_info)
def insert_patient(patient:Patient):
    print(patient.name)
    print(patient.age)

insert_patient(Patient1)