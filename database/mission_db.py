from database.db_connection import DB_connection
from pydantk_vld import CheckMission

class MissionDB:
    def __init__(self):
        self.db = DB_connection()
    
    def create_mission(self,data : CheckMission):
        if  1 <= data.importance <= 10 and 1 <= data.difficulty <= 10:
            risk_score = data.difficulty * 2 + data.importance
            if risk_score <= 9:
                risk_level = "LOW"
            elif 10 <= risk_score <= 17:
                risk_level = "MEDIUM"
            elif 18 <= risk_score <= 24:
                risk_level = "HIGH"
            else:
                risk_level = "CRITICAL"
            cursor = self.db.get_connection().cursor(dictionary=True)
            cursor.execute("""
                        insert INTO missions (title,description,location,difficulty,importance,status,risk_level,assigned_agent_id)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                        ,(data.title,data.description,data.location,data.difficulty,data.importance,data.status,risk_level,data.assigned_agent_id)
                        )
            cursor._connection.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return self.get_mission_by_id(new_id)
        raise ValueError("importance and difficulty most be btwwen 1 an 10")
    
    def get_all_missions(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from missions")
        res = cursor.fetchall()
        cursor.close()
        return res if res else []
    
    def get_mission_by_id(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from missions where id = %s",(id,))
        res = cursor.fetchone()
        cursor.close()
        return res
    
    def assign_mission(self,m_id : int,a_id):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select is_active from agents where id = %s",(a_id,))
        res = cursor.fetchone()
        if res and res["is_active"] == True:
            cursor.execute("update missions set assigned_agent_id = %s where id = %s",(a_id,m_id))
            cursor._connection.commit()
            cursor.close()
            return "mission assigned seccessfully"
        cursor.close()
        return "this agent cant get a mission"
    
    def update_mission_status(self,id : int, status : str):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("update missions set status = %s where id = %s",(status,id))
        cursor._connection.commit()
        cursor.close()

    def get_open_missions_by_agent(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from missions where assigned_agent_id = %s and status in('ASSIGNED' , 'IN_PROGRESS')",(id,))
        res = cursor.fetchall()
        cursor.close()
        return res if res else []

    def count_all_missions(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) as total from missions")
        res = cursor.fetchone()
        cursor.close()
        return res["total"] if res else 0
    
    def count_by_status(self, status : str):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) as total from missions where status = %s",(status,))
        res = cursor.fetchone()
        cursor.close()
        return res["total"] if res else 0
    
    def count_open_missions(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) as total from missions where status in ('ASSIGNED' , 'IN_PROGRESS')")
        res = cursor.fetchone()
        cursor.close()
        return res["total"] if res else 0
    
    def count_critical_missions(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) as total from missions where risk_level = 'CRITICAL'")
        res = cursor.fetchone()
        cursor.close()
        return res["total"] if res else 0
    
    def get_top_agent(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents order by completed_missions desc limit 1")
        res = cursor.fetchone()
        cursor.close()
        return res