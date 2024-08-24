import uvicorn

from application.api import create_api
from application.db_config import mongo_start_connection

mongo_start_connection()
api = create_api()


if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=8000, log_level="info")
