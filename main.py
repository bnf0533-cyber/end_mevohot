from database.db_connection import DB_connection
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_roules import router as reports_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()
db_connect = DB_connection()
app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(reports_router)

if __name__ =="__main__":
    db_connect.create_database()
    db_connect.create_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
