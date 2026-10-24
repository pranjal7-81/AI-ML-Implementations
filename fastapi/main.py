from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field,computed_field
from typing import Annotated,Literal,Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str,Field(...,description="ID of patient",examples=['P001'])]
    name: Annotated[str,Field(...,description="Name of the patient")]
    city : Annotated[str,Field(...,description="nameo of city where patient belongs to")]
    age : Annotated[int,Field(...,gt = 0,lt=120,description="Age of the pateint")]
    gender : Annotated[Literal['male','female','others'],Field(...,description="Gender of the patient")]
    height : Annotated[float,Field(...,gt = 0,description="height of the patient in mtrs")]
    weight : Annotated[float,Field(...,gt=0,description="Weight of the patient in Kgs")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2) 
        return bmi
    @computed_field
    @property
    def verdict(self) -> str:
        if(self.bmi<18.5):
            return "underweight"
        elif(self.bmi<25):
            return "Normal"
        elif(self.bmi<30):
            return "OverWeight"
        else:
            return "Obese"
        
        
from typing import Optional

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[
        Optional[Literal['male', 'female']],
        Field(default=None)
    ]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    

@app.get("/")
def root():
    return {"message": "Patient management system is running."}


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

def hello():
    return {"message": "Patient management system is running."}

@app.get("/about")

def about():
    return {"message": "A fully functional patient management system built with FastAPI."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/view/{patient_id}")

def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve",examples="P001")):
    #load all pateint data
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
    
@app.get("/sort")
def sort_patients(sort_by :str = Query(..., description="Sort basis on height,weight and bmi"),order = Query("asc", description = "ascending order")):
    valid_fields = ['height', 'weight', 'bmi']
    if(sort_by not in valid_fields):
        raise HTTPException(status_code=400, detail = f"Invalid sort field. Must be one of: height, weight, bmi , Select from {valid_fields}")
    if(order not in ['asc', 'desc']):
        raise HTTPException(status_code=400, detail = f"Invalid order. Must be one of: asc, desc")
    
    data = load_data()
    sort_order = True if order == 'asc' else False
    sorted_data = sorted(data.values(),key = lambda x: x.get(sort_by,0),reverse = False)
    return sorted_data
    
@app.post('/create')
def create_patient(patient: Patient):
    #load existing data
    data = load_data()
    
    #check if patient already exits
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")
    
    #new patient add to the data in form of dict
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    #save this in json also
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'patient created sucessfully'})


@app.put('/edit/{patient_id}')

def update_patient(patient_id : str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value
        
        
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
        
    ##pydantic obj -> dict
    patient_pydantic_obj.model_dump(exclude={'id'})
    ##add this dict to data
    data[patient_id] = existing_patient_info
    
    #save data
    save_data(data)
    return JSONResponse(status_code=200,content={'message':"Patient Updated..."})


@app.delete('/delete/{patient_id}')

def delete_patient(patient_id : str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")
    del data[patient_id]
    
    save_data(data)
    return JSONResponse(status_code=200,content="Patient Deleted.")


     
    
    
    
    
    