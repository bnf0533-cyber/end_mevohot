from database.agent_db import AgentDB
from fastapi import APIRouter , HTTPException
from pydantk_vld import CheckAagent
from logs.logeers import logger

router = APIRouter(tags=["AGENT"])
agent_db = AgentDB()


@router.post("/agents")
def create_agent(data : CheckAagent):
    logger.info("POST /agents called")
    try:
        logger.info(f"inserting agent {data.name}")
        agent_db.create_agent(data)
        logger.info(("POST/agents finished"))
    except Exception as e:
        logger.error(f"error: {e}")
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/agents")
def get_all_agents():
    logger.info("GET/agents called")
    res = agent_db.get_all_agents()
    logger.info("GET /agents finished")
    return res if res else []

@router.get("/agents/{id}")
def get_agent_by_id(id : int):
    logger.info(f"/GET /agents/{id} called")
    res = agent_db.get_agent_by_id(id)
    if res:
        logger.info(f"/GET /agents/{id} finshed")
        return res
    logger.error((f"agent not found : {id}"))
    raise HTTPException(status_code=404,detail="id not found")

@router.put("agents/{id}")
def update_agent(id : int, data : CheckAagent):
    logger.info(f"PUT/ agents/{id} called")
    try:
        logger.info(f"updating agent {id}")
        agent_db.update_agent(id , data)
        logger.info(f"PUT/ agents/{id} finished")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=400,detail=str(e))
    
@router.put("/agent/{id}/deactivate")
def deactivare_agent(id : int):
    logger.info(f"/agent/{id}/deactivate called")
    try:
        logger.info(f"deactivating agent {id}")
        res = agent_db.deactivate_agent(id)
        logger.info(f"agent {id} deactivate")
        return res
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=400 , detail=str(e))

@router.get("/agent/{id}/performance")
def get_preformance_agent(id : int):
    logger.info("GET/agent/{id}/performance called")
    res = agent_db.get_agent_performence(id)
    logger.info("GET/agent/{id}/performance finished")
    return res