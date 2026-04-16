from typing import Optional
from pydantic import BaseModel

class Agent(BaseModel):
    id: int
    group: Optional[int] = None
    income: Optional[float] = None
    age: Optional[int] = None
    building_type: Optional[str] = None
    build_age: Optional[int] = None  # building age category 1-10
    energy_std: Optional[str] = None  # energy standard of building
    subsidy: Optional[float] = None  # subsidy amount
    info_pas: Optional[float] = None  # awareness about passive house
    info_s11: Optional[float] = None  # awareness about S11
    municipality: Optional[str] = None
    state: Optional[str] = None   
                    # 1,2,3 → ADOPTED
                    # 4,5 → AWARE
                    # 6 → UNAWARE