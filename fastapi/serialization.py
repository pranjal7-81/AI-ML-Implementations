from pydantic import BaseModel

class Address(BaseModel):
    city : str
    state : str
    pin : str

class Patient(BaseModel):
    name: str
    age: int 
    address : Address
    
address_dict = {'city': 'New York', 'state': 'NY', 'pin': '10001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'John Doe', 'age': 40, 'address': address1}

patient1 = Patient(**patient_dict) 

print(patient1)
print(patient1.age)
print(patient1.address.city)
print(patient1.address.pin)

temp = patient1.model_dump(exclude = {'name'})
print(temp)
print(type(temp))
