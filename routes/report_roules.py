from fastapi import APIRouter
from database.agent_db import AgentDB
from database.mission_db import MissionDB
from logs.logeers import logger
from database.db_connection import DB_connection

router = APIRouter(tags=["REPORTES"])
agent = AgentDB()
mission = MissionDB()
db_connect = DB_connection()



@router.get("/reports/summary")
def get_reports():
    logger.info("GET/ reportes / summary called")
    res ={"active_agents_count" : {agent.count_active_agents()},
                "total_missions": {mission.count_all_missions()},
                "open_missions": {mission.count_open_missions()},
                "completed_missions": {mission.count_by_status('COMPLETED')},
                "failed_missions": {mission.count_by_status('FAILED')},
                "critical_missions": {mission.count_critical_missions()}}
    logger.info("GET /reports/summary finished")
    return res

@router.get("/reports/mission-by-status")
def get_mission_by_status(status : str):
    logger.info("GET/reports/mission-by-status for {status} called")
    res = mission.count_by_status(status=status)
    logger.info("GET/reports/mission-by-status for {status} finished")
    return res

@router.get("/reports/top-agent")
def get_top_agent():
        cursor = db_connect.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents order by completed_missions desc limit 1")
        res = cursor.fetchone()
        cursor.close()
        return res if res else []