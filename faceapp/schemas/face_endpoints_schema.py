# schemas.py
from pydantic import BaseModel, Field

class FaceRegistrationSchema(BaseModel):
    name: str = Field(..., description="First name of the person")
    lastName: str = Field(..., description="Last name of the person")

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "lastName": "Doe"
            }
        }
