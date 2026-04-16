from typing import Optional
from pydantic import BaseModel

class Agent(BaseModel):
    id: int
    group: Optional[int] = None
    income: Optional[float] = None
    age: Optional[int] = None
    building_type: Optional[str] = None
    municipality: Optional[str] = None
    state: Optional[str] = None   
                    # 1,2,3 → ADOPTED
                    # 4,5 → AWARE
                    # 6 → UNAWARE