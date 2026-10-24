
from pydantic import AnyUrl, BaseModel , EmailStr, Field ,field_validator
from typing import List , Dict , Optional , Annotated 


class Patient(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50,title='Patient Name',description='Name of the patient in less than 50 characters',examples = ['John Doe', 'Jane Smith'])]
    age: Annotated[int, Field(gt=0)]
    email: EmailStr
    weight: Annotated[float, Field(gt=0)]
    linkedin_url : AnyUrl
    married: Annotated[bool, Field(title='Married Status', description='Is the patient married or not?')]
    allergies: Annotated[Optional[List[str]], Field(max_length=5)]
    contact_details: Dict[str, str]
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains = ['hdfc.com' , 'icici.com' , 'sbi.com']
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError(f'Email domain must be one of {valid_domains} .')
        
        return value
     
     
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.linkedin_url)
    print(patient.married)
    print(patient.allergies)
    print('inserted')
    
patient_info = {'name': 'John Doe', 'age': 40 , 'email': 'john.doe@hdfc.com', 'weight': 70.5, 'linkedin_url': 'https://www.linkedin.com/in/johndoe', 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details': {'phone': '123-456-7890'}}


patient1 = Patient(**patient_info)


insert_patient(patient1)
