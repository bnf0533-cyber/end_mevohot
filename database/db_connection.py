import mysql.connector

class DB_connection:
    def __init__(self):
        self.confing = {
            "host" : "127.0.0.1",
            "potr" : 3306,
            "user" : "root",
            "databse" : "db_Intelligence"
        }
        self._connection = None
    
    def get_connection(self):
        if self._connection:
            return self._connection
        self._connection = mysql.connector.connect(**self.confing)
        return self._connection
    
    def create_database(self):
        cursor = self.get_connection().cursor(dictionary=True)
        cursor.execute("CREATE DATABASE IF NOT EXISTS db_Intelligence")
        cursor.close()
        self._connection.commit()

    def create_tables(self):
        cursor = self.get_connection().cursor(dictionary=True)
        self.confing["database"] = "db_Intelligence"
        cursor.execute("""
                        CREATE TABLE if NOT exists agents(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(50),
                            spectialy VARCHAR(150),
                            is_active BOOLEAN DEFAULT True,
                            completed_mission INT DEFAULT 0,
                            failed_mission INT DEFAULT 0,
                            agent_rank ENUM('Junior', 'Senior', 'Commander')
                            )"""
                        )
        
        cursor.execute("""
                        CREATE TABLE if NOT exists missions(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            title VARCHAR(50),
                            description TEXT,
                            location VARCHAR(100),
                            difficulty INT,
                            importance INT,
                            status VARCHAR(50) DEFAULT 'new',
                            risk_level VARCHAR(10),
                            assigned_agens_id INT DEFAULT NULL
                            )"""
                        )
