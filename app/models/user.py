

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, ConfigDict

# ---------------------------
#  CREATE USER REQUEST
# ---------------------------


class CreateUserRequest(BaseModel):
    name: str
    email:str 
    number: Optional[str]= None
    model_config = ConfigDict(from_attributes=True)

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    number: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    name:str 
    email:str
    number: Optional[str] = None
    created_at: datetime
    
