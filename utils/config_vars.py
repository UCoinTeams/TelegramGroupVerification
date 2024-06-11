import yaml
from redis import Redis
from .sqlite_orm import SQLite
from .data_api import DataAPI

with open("data/config.yaml", "r") as f:
    config: dict = yaml.safe_load(f)

LOG_LEVEL = config["LOG_LEVEL"]

sql = SQLite()

redis = Redis(
    host=config["REDIS"]["HOST"],
    port=config["REDIS"]["PORT"],
    db=config["REDIS"]["REDIS_DATABASE"],
)
