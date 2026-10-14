from fastapi import FastAPI
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