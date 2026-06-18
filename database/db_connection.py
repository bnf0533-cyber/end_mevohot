import mysql.connector

class DB_connection:
    def __init__(self):
        self.config = {
            "host" : "127.0.0.1",
            "port" : 3306,
            "user" : "root",
            "password" : "1234",
            "database" : "Intelligence_db"
            
        }
        self.db_name = "Intelligence_db"
        self._connection = None
    
    def get_connection(self):
        if self._connection:
            return self._connection
        self._connection = mysql.connector.connect(**self.config)
        return self._connection
    
    def create_database(self):
        cursor = self.get_connection().cursor(dictionary=True)
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS Intelligence_db")
        self.config["database"] = self.db_name
        cursor.close()
        self._connection = None


    def create_tables(self):
        cursor = self.get_connection().cursor(dictionary=True)
        cursor.execute("""
                        CREATE TABLE if NOT exists agents(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(50),
                            specialty VARCHAR(150),
                            is_active BOOLEAN DEFAULT True,
                            completed_missions INT DEFAULT 0,
                            failed_missions INT DEFAULT 0,
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
                            status VARCHAR(50) DEFAULT 'NEW',
                            risk_level VARCHAR(10),
                            assigned_agent_id INT DEFAULT NULL
                            )"""
                        )
        cursor.close()