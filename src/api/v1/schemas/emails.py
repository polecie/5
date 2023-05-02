from pydantic import BaseModel, EmailStr


class EmailRequest(BaseModel):
    email: EmailStr
    password: str  # TODO: хранить зашифрованными
    provider_id: int

    class Config:
        orm_mode = True


class EmailResponse(BaseModel):
    id: int
    email: EmailStr
    provider_id: int

    class Config:
        orm_mode = True
