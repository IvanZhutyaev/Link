from pydantic import BaseModel, Field



class UserModel(BaseModel):
    User_name: str = Field( max_length=50)
    Phone_number: str = Field( max_length=12, pattern=r"^\+?\d{10,12}$")
    password: str = Field( max_length=255)

class UserResponse(UserModel):
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    phone: str
    password: str