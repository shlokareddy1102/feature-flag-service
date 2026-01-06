from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True
        

class FeatureCreate(BaseModel):
    name: str
    enabled: bool = False
    rollout_percentage: int = 0


class FeatureUpdate(BaseModel):
    enabled: bool
    rollout_percentage: int


class FeatureResponse(BaseModel):
    id: int
    name: str
    enabled: bool
    rollout_percentage: int

    class Config:
        from_attributes = True
