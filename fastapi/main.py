from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Patient management system is running."}


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

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
    
    
    