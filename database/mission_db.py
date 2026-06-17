from database.db_connection import DB_connection
from pydantk_vld import CheckMission

class MissionDB:
    def __init__(self):
        self.db = DB_connection()
    
    def create_mission(self,data : CheckMission):
        if not 1 < data.importance > 10 and 1 < data.difficulty > 10:
            risk_level = data.difficulty * 2 + data.importance
            if 1 < risk_level < 9:
                risk_level = "LOW"
            elif 10 <= risk_level <= 17:
                risk_level = "MEDIUM"
            elif 18 <= risk_level <= 24:
                risk_level = "HIGH"
            elif risk_level >= 25:
                risk_level = "CRITICAL"
            cursor = self.db.get_connection().cursor(dictionary=True)
            cursor.execute("""
                        insert INTO missions (title,description,location,difficulty,importance,status,aassigned_agens_id)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                        ,(data.title,data.description,data.location,data.difficulty,data.importance,risk_level,data.assigned_agens_id)
                        )
            cursor._connection.commit()
            res = cursor.fetchone()
            cursor.close()
            return res
        raise ValueError("importance and difficulty most be btwwen 1 an 10")
    
    def get_all_mission(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from missions")
        res = cursor.fetchall()
        cursor.close()
        return res
    
    def assign_mission(self,m_id : int,a_id):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select is_active from agents where id = %s",(a_id,))
        res = cursor.fetchone()
        if not res["is_active"] == False:
            cursor.execute("update missions set assigned_agens_id = %s where id = %s",(a_id,m_id))
            cursor._connection.commit()
            cursor.close()
        return "this agent cant get a mission"
    
    def update_mission_status(self,id : int, status : CheckMission):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("update missions set status = %s where id = %s",(status,id))
        cursor._connection.commit()
        cursor.close()

    def get_open_missions_by_agent(self,id : int):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select status from missions where id = %s",(id,))
        res = cursor.fetchall()
        cursor.close()
        return res

    def count_all_misiion(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) from missions")
        res = cursor.fetchone()
        cursor.close()
        return res
    
    def count_by_status(self, status : CheckMission):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) from missions where status = %s",(status,))
        res = cursor.fetchone()
        cursor.close()
        return res
    
    def count_open_missions(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) from missions where status = IN_PROGRESS")
        res = cursor.fetchone()
        cursor.close()
        return res
    
    def count_critical_missions(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select count(*) from missions where risk_level = CRITICAL")
        res = cursor.fetchone()
        cursor.close()
        return res
    
    def get_top_agent(self):
        cursor = self.db.get_connection().cursor(dictionary=True)
        cursor.execute("select * from agents order by completed_missions desc limit 1")
        res = cursor.fetchone()
        cursor.close()
        return res