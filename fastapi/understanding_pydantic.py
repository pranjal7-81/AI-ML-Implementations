from pydantic import AnyUrl, BaseModel , EmailStr, Field ,gt
from typing import List , Dict , Optional , Annotated ,title, description
class Patient(BaseModel):
    name: str = Annotated[str, Field(min_length=1, max_length=50),title='Patient Name',description='Name of the patient in less than 50 characters']
    age: int = Field(gt=0)
    email: EmailStr
    weight: float = Field(gt=0)
    linkedin_url : AnyUrl
    married: Optional[bool] = None
    allergies: Optional[List[str]] = Field(max_length=5)
    contact_details: Dict[str, str]
     
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.linkedin_url)
    print(patient.married)
    print(patient.allergies)
    print('inserted')
    
patient_info = {'name': 'John Doe', 'age': 40 , 'email': 'john.doe@example.com', 'weight': 70.5, 'linkedin_url': 'https://www.linkedin.com/in/johndoe', 'allergies': ['pollen', 'dust'], 'contact_details': {'phone': '123-456-7890'}}


patient1 = Patient(**patient_info)

insert_patient(patient1) 