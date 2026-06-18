from database.db_connection import DB_connection
from pydantk_vld import CheckAagent


class AgentDB:
    def __init__(self):
        self.db = DB_connection()
    
    def create_agent(self,data : CheckAagent):
        if data.agent_rank not in ["Junior", "Senior" , "Commander"]:
            raise ValueError("rank isnt correct")
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("""
                    insert INTO agents (name,specialty,is_active,completed_missions,failed_missions,agent_rank)
                    VALUES (%s,%s,%s,%s,%s,%s)"""
                    ,(data.name,data.specialty,data.is_active,data.completed_missions,data.failed_missions,data.agent_rank)
                    )
        cursor._connection.commit()
        new_agent = cursor.lastrowid
        cursor.close()
        return self.get_agent_by_id(new_agent)
    
    def get_all_agents(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents")
        res = cursor.fetchall()
        cursor.close()
        return res if res else []
    
    def get_agent_by_id(self,id:int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents where id = %s",(id,))
        res = cursor.fetchone()
        cursor.close()
        return res
    
    def update_agent(self, id : int , data : CheckAagent):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("""
                    UPDATE agents SET
                    name = %s,
                    specialty = %s,
                    is_active = %s,
                    completed_missions = %s,
                    failed_missions = %s,
                    agent_rank = %s
                    where id = %s
                    """,(
                    data.name,
                    data.specialty,
                    data.is_active,
                    data.completed_missions,
                    data.failed_missions,
                    data.agent_rank,
                    id,))
        cursor._connection.commit()
        cursor.close()
        return "agent updated successfully"
    
    def deactivate_agent(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("update agents set is_active = False where id = %s",(id,))
        cursor._connection.commit()
        cursor.close()
        return "agent deactivated successfully"
    
    def increment_completed(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("update agents set completed_missions = completed_missions + 1 where id = %s",(id,))
        cursor._connection.commit()
        cursor.close()
        return "completed missions incremented successfully"

    def increment_failed(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("update agents set failed_missions = failed_missions + 1 where id = %s",(id,))
        cursor._connection.commit()
        cursor.close()
        return "failed missions incremented successfully"

    def get_agent_performance(self,id : int):
        agent = self.get_agent_by_id(id)
        if not agent:
            return None
        completed = agent["completed_missions"]
        failed = agent["failed_missions"]
        total = completed + failed
        success_rate = 0
        if total > 0:
            success_rate = (completed / total) * 100
        return {
            "completed" : completed,
            "failed" : failed,
            "total" : total,
            "success_rate" : success_rate
        }
        
    def count_active_agents(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) as active_count from agents where is_active = True")
        res = cursor.fetchone()
        cursor.close()
        return res["active_count"] if res else 0