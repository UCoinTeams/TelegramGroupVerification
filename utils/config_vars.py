import yaml
from redis import Redis
from .sqlite_orm import SQLite
from .data_api import DataAPI

with open("data/config.yaml", "r") as f:
    config: dict = yaml.safe_load(f)

LOG_LEVEL = config["LOG_LEVEL"]

d_api = DataAPI(
    u2_cookie=config["U2_COOKIE"],
    api_uesr_id=config["API_USER_ID"],
    api_token=config["API_TOKEN"],
    bark_uel=config["BARK_URL"],
)

sql = SQLite()

redis = Redis(
    host=config["REDIS"]["HOST"],
    port=config["REDIS"]["PORT"],
    db=config["REDIS"]["REDIS_DATABASE"],
)
