from pydantic import BaseModel, Field



class ZastroyModel(BaseModel):
    Company_name : str = Field(max_length=50)
    INN: int  = Field()
    OGRN: int  = Field()
    Adress: str = Field(max_length=255)
    User_name: str = Field(max_length=255)
    password:str=Field(max_length=255)


class ZastroyResponse(ZastroyModel):
    id: int

    class Config:
        from_attributes = True



class ZastroyLogin(BaseModel):
    inn: int
    password: str


