from fastapi import APIRouter ,HTTPException
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from pydantk_vld import CheckMission
from logs.logeers import logger

router = APIRouter(tags=["MISSION"])
mission_db = MissionDB()
agent_db = AgentDB()


@router.post("/missions")
def create_mission(data : CheckMission):
    logger.info("POST/ miisions called")
    try:
        logger.info(f"inserrting mission {data.title}")
        mission_db.create_mission(data)
        logger.info("POST/ missions finished")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/missions")
def get_all_missions():
    logger.info("GET/ missions called")
    try:
        logger.info("GET/ mission start")
        res = mission_db.get_all_missions()
        logger.info("GET/ missions finished")
        return res
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/missions/{id}")
def get_miison_by_id(id :int):
    logger.info(f"GET/mission/{id} called")
    mission = mission_db.get_mission_by_id(id)
    if mission:
        logger.info(f"INFO/missoin/{id}")
        return mission
    logger.error(f"miision not found : {id}")
    raise HTTPException(status_code=404,detail=f"miision {id} not found")

@router.put("/mission/{id}/assign/{agent_id}")
def assign_mission(id : int , agent_id : int):
    logger.info(f"PUT/mission/{id}/assigan/{agent_id} called")
    try:
        agent = agent_db.get_agent_by_id(agent_id)
        mission = mission_db.get_mission_by_id(id)
        if not mission:
            raise HTTPException(status_code=404,detail=f"miision {id} not found")
        if not agent:
            raise HTTPException(status_code=404 , detail=f"agent {id} not found")
        if not mission[0]["NEW"]:
            raise HTTPException(status_code=400 , detail=f"mission not available")
        if not agent[0]["is_active"]:
            raise HTTPException(status_code=400 , detail="agent is active")
        active_mission = mission_db.count_open_missions()
        if active_mission and active_mission["count(*)"] >= 3:
            raise HTTPException(status_code=400,detail="agent has reached maximum missions")
        if not mission["risk_level"] == "CRITIAL" and agent["agent_rank"] == "commander":
            raise HTTPException(status_code=400,detail="only commander can handle critical missions")
        logger.info(f"strarting assigning misiion {id} for agent {agent_id}")
        mission_db.assign_mission(id,agent_id)
        logger.info(f"finished assigning misiion {id} for agent {agent_id}")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=400,detail=str(e))

@router.put("/missions/{id}/start")
def start_mission(id :int  , status :CheckMission):
    mission = mission_db.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=404 , detail=f"agent {id} not found")
    if not mission["status"] == "ASSIGNED":
        raise HTTPException(status_code=400 , detail=f"mission already assigned")
    try:
        logger.info(f"start misiion starting")
        mission_db.update_mission_status(id,status="IN_PROGRES")
        logger.info("start mission finisshed")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=400 , detail=str(e))
    
@router.put("/missions/{id}/complete")
def complete_mission(id: int):
    mission = mission_db.get_mission_by_id(id)
    agent = agent_db.get_agent_by_id(mission)
    logger.info(f"PUT/missions/{id}/ called")
    try:
        logger.info(f"complete mission {id} starting")
        mission_db.update_mission_status(mission)
        agent_db.increment_completed(agent)
        logger.info(f"complete mission {id} finushed")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=400,detail=str(e))
    
@router.put("/mission/{id}/fail")
def failed_mission(id: int):
    logger.info(f"/missions/{id}/fail called")
    mission = mission_db.get_mission_by_id(id)
    agent = agent_db.get_agent_by_id(mission)
    try:
        logger.info("failed mission starting")
        mission_db.update_mission_status(mission)
        agent_db.increment_failed(agent)
        logger.info("failed mission finished")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=400,detail=str(e))

@router.put("/missions/{id}/cencel")
def cencel_mission(id : int):
    logger.info(f"PUT/ missions/{id}/cencel called")
    mission = mission_db.get_mission_by_id(id)
    try:
        logger.info("startin cencel mission")
        mission_db.update_mission_status(mission,status="CANCELLD")
        logger.info("cecncel mission finished")
    except Exception as e:
        logger.error(f"error :  {e}")
        raise HTTPException(status_code=400,detail=str(e))
    

