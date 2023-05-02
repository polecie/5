import datetime
from pydantic import BaseModel, validator


class UserRequest(BaseModel):
    id: int

    @validator("id")
    def id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("id must be positive")
        return v

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        # schema_extra = {
        #     "example": {
        #         "id": 123456789,
        #         "created_at": "2021-10-10T00:00:00"
        #     }
        # }
