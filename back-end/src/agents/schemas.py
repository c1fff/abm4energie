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
    foerderung: float = 0.3  # SUB
    trigger: float = 0.0  # TRIG_1-TRIG_4
    social_influence: float = 0.0  # INFO_S11
    info_sources: float = 0.0  # INFO_S1-INFO_S10, INFO_S12
    known_households: float = 0.0  # INFO_PAS
    municipality: Optional[str] = None
    state: Optional[str] = None
    # 1,2 -> ADOPTED
    # 3,4 -> AWARE
    # 5,6 -> UNAWARE
