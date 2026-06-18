from pydantic import BaseModel
from typing import Literal

rank = Literal["Junior","Senior","Commander"]

class CheckAagent(BaseModel):
    id : int | None = None
    name : str
    specialty : str
    is_active : bool = True
    completed_missions : int = 0
    failed_missions : int = 0
    agent_rank : rank

class CheckMission(BaseModel):
    id : int | None = None
    title : str
    description : str
    location : str
    difficulty : int
    importance : int
    status : Literal["NEW","ASSIGNED","IN_PROGRESS","COMPLETED","FAILED","CANCELLED"] = "NEW"
    risk_level : str | None = None
    assigned_agent_id : int | None = None