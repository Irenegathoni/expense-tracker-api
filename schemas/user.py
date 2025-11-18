from pydantic import BaseModel,EmailStr,Field,validator
class UserRegister(BaseModel):  #basemodel is the base class for creating validation models
    name:str =Field(...,min_length=1,max_length=100)
    email:EmailStr #validates the email format automatically
    password:str = Field(...,min_length=8,max_length=100)

    @validator('name')
    def name_must_not_be_empty(cls,v):
        if not v.strip():
            raise ValueError('Name cannot be empty or just spaces')
        return v.strip() #v.strip() removes spaces from start and end
    
    
    @validator('password')
    def password_strength(cls,v):
        #password must have atleast one letter and one number
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain atleast one letter')
        return v

class UserLogin(BaseModel):
    email:EmailStr
    password:str =Field(...,min_length=1)
