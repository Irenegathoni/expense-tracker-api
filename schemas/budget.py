from pydantic import BaseModel, Field, validator
import re
from datetime import date
class BudgetCreate(BaseModel):
    category:str =Field(...,min_length=1,max_length=50)
    monthly_limit:float = Field(...,gt=0)
   
    @validator('category')
    def category_not_empty(cls,v):
        #category cannot be just spaces and allows underscores
        if not v.strip():
            raise ValueError('Category cannot be empty')
        #allow letters,spsces, numbers and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$',v):
            raise ValueError('Category can only contain letters,numbers,spaces and underscore')
        return v.strip()
    @validator('monthly_limit')
    def limit_two_decimals(cls,v):
        if round(v,2) !=v:
            raise ValueError('Monthly limit can only have up to 2 decimal place')
        return round(v,2)
    

class BudgetUpdate(BaseModel):
    category:str=Field(None,min_length=1,max_length=50)
    monthly_limit:float=Field(None,gt=0)

    @validator('category')
    def validate_category(cls,v):
        if v is not None:
            if not v.strip():
                raise ValueError('Category cannot be updated')
            if not re.match(r'^[a-zA-Z0-9_]+$',v):
                raise ValueError('Category can only contain letters, numbers,spaces and underscores')
            return v.strip()
        return v
    
    @validator('monthly_limit')
    def validate_monthly_limit(cls,v):
        if v is not None:
            if round(v,2) !=v:
                raise ValueError('Monthly limit can only have up to 2 decimal places')
            return round(v,2)
        return v
    
class BudgetStatus(BaseModel):
    category:str
    limit:float
    spent:float
    remaining:float
    over_budget:bool   
    
                    


    

    
