from database.db_connection import DB_connection
from pydantk_vld import CheckAagent


class AgentDB:
    def __init__(self):
        self.db = DB_connection()
    
    def create_agent(self,data : CheckAagent):
        if data.agent_rank:

            cursor = self.db.get_connection().cursor(dictionary=True)
            cursor.execute("""
                        insert INTO agents (name,spectialy,is_active,completed_mission,failed_mission,agent_rank)
                        VALUES (%s,%s,%s,%s,%s,%s)"""
                        ,(data.name,data.spectialy,data.is_active,data.completed_mission,data.failed_mission,data.agent_rank)
                        )
            cursor._connection.commit()
            cursor.close()
        raise ValueError("rank isnt correct")

    def get_all_agents(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents")
        res = cursor.fetchall()
        cursor.close()
        return res
    
    def get_agent_by_id(self,id:int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents where id = %s",(id,))
        res = cursor.fetchall()
        cursor.close()
        return res
    
    def update_agent(self, id : int , data : CheckAagent):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("""
                    UPDATE agents SET
                    name = %s,
                    spectialy = %s,
                    is_active = %s,
                    completed_mission = %s,
                    failed_mission = %s,
                    agent_rank = %s
                    """,(
                    data.name,
                    data.spectialy,
                    data.is_active,
                    data.completed_mission,
                    data.failed_mission,
                    data.agent_rank,
                    id,),)
        cursor._connection.commit()
        cursor.close()
    
    def deactivate_agent(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("update agents set is_active = False where id = %s",(id,))
        cursor._connection.commit()
        cursor.close()
    def increment_completed(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("update agents set completed_mission = completed_mission + 1 where id = %s",(id,))
        cursor._connection.commit()
        cursor.close()

    def increment_failed(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("update agents set failed_mission = failed_mission + 1 where id = %s",(id,))
        cursor._connection.commit()
        cursor.close()

    def get_agent_performence(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents where id = %s",(id,))
        res = cursor.fetchone()
        performence = {"cmpleated" : res["completed_mission"],
                        "failed" : res["failed_mission"],
                        "total" : res["completed_mission"] + res["failed_mission"],
                        "success_rate" : (res["completed_mission"] / res["completed_mission"] + res["failed_mission"]) / 100
                        }
    def count_active_agents(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents where is_active = True")
        res = cursor.fetchall()
        cursor.close()
        return res