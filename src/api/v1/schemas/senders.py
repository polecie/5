from pydantic import BaseModel, EmailStr


class SenderRequest(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class SenderResponse(BaseModel):
    id: int
    email: EmailStr
    user_id: int

    class Config:
        orm_mode = True
