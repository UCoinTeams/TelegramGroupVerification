import yaml
import uvicorn
from fastapi import FastAPI, HTTPException

from utils.sqlite_orm import SQLite


with open("data/config.yaml", "r") as f:
    config: dict = yaml.safe_load(f)

app = FastAPI()
sql = SQLite()


@app.get("/user")
async def get_user(tg_id: int = None, u2_id: int = None):
    data = sql.inqury_user(tg_id, u2_id)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    send_data = []
    for i in data:
        send_data.append(
            {
                "tg_id": i[1],
                "u2_id": i[2],
                "language": i[3],
                "record_time": i[4],
            }
        )
    return send_data

@app.middleware("http")
async def permission_monitoring(request, call_next):
    if request.headers.get("Content-Auth") not in config["API_SERVER"]["AUTH_KEY"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    sql.insert_admin_log(0, request.headers.get("Content-Auth"), f"API 查询 {request.url.query}", 0, 0)
    response = await call_next(request)
    return response



def start_server():
    uvicorn.run(
        app, host=config["API_SERVER"]["HOST"], port=config["API_SERVER"]["PORT"]
    )
