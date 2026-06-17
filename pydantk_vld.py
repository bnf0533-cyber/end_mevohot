from pydantic import BaseModel
from typing import Literal
Rank = Literal["""
        Junior,
        Senior,
        Commander
        """]
class CheckAagent(BaseModel):
    id : int
    name : str
    spectialy : str
    is_active : bool
    completed_mission : int
    failed_mission : int
    agent_rank : Rank

class CheckMission(BaseModel):
    id : int
    title : str
    description : str
    location : str
    difficulty : int
    importance : int
    status : Literal["NEW","ASSIGNED","IN_PROGRESS","COMPLETED","FAILED","CANCELLED"]
    assigned_agens_id : int