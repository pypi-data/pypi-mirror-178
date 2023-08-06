from pydantic import BaseModel

class VariableBase(BaseModel):
    name: str
    description: str
    unit: str

class VariableCreate(VariableBase):
    pass

class Variable(VariableBase):
    id: int
    class Config:
        orm_mode = True
