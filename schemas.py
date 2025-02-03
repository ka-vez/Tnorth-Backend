from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str 
    is_active: bool = Field(default=False)
    role: str = Field(default="user")
    phone_number: str  
