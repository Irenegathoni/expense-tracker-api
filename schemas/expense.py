from pydantic import BaseModel,Field,validator
import re
from datetime import datetime

class ExpenseCreate(BaseModel):
    description:str =Field(...,min_length=1,max_length=200)
    amount:float=Field(...,gt=0) #gt=greater than 0
    category:str=Field(...,min_length=1,max_length=50)
    date:str

    @validator('description')
    def description_not_empty(cls,v):
        #description cannot be just spaces
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()
        
    @validator('amount')
    def amount_has_max_two_decimals(cls,v):
        if round(v,2) != v:
           raise ValueError('Amount can only have up to 2 decimal places')
        return round(v,2)
    
    @validator('category')
    def validate_category(cls,v):
        #category cannot be just spaces and allows underscores 
        if not v.strip():
            raise ValueError('Category cannot be empty') 
        #allow letters,numbers,spaces and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$',v):
            raise ValueError('Category can only contain letters,numbers,spaces, and underscores')
        return v.strip()
    

    @validator('date')
    def validate_date_format(cls,v):
        #the date format is DD-MM-YYYY
        try:
            #parsing the date in DD-MM-YYYY
            parsed_date=datetime.strptime(v,'%d-%m-%Y')
            return v
        except ValueError:
            raise ValueError('Date must be in DD-MM-YYYY format(e.g.,15-02-2003)')


class ExpenseUpdate(BaseModel):
    #all fields are optional, user might only want to update one fiels
    description:str = Field(None,min_length=1,max_length=200)
    amount:float=Field(None,gt=0)
    category:str=Field(None,min_length=1,max_length=50)
    date:str= None

    @validator('description')
    def description_not_empty(cls,v):
        #description cannot be just spaces
        if v is not None:
            if not v.strip():
                raise ValueError('Description cannot be empty')
            return v.strip()
        return v
    
    @validator('amount')
    def amount_has_max_two_decimals(cls,v):
        if v is not None:
            if round(v,2) !=v:
                raise ValueError('Amount can only have up to 2 decimal places')
            return round(v,2)
        return v
    
    @validator('category')
    def validate_category(cls,v):
        if v is not None:
            if not v.strip():
                raise ValueError('Category cannot be empty')
            #allowing letters,numbers,spaces and underscores
            if not re.match(r'^[a-zA-Z0-9_]+$',v):
                raise ValueError('Category can only contain letters, numbers,spaces and underscores')
            return v.strip()
        return v
    

    @validator('date')
    def validate_date_format(cls,v):
        if v is not None:
            try:

                #parse the date in DD-MM-YYYY Format
                datetime.strptime(v,'%d-%m-%Y')
                return v
            except ValueError:
                raise ValueError('Date must be in DD-MM-YYYY format (e.r., 15-02-2003)')
        return v
        
        
    


    
