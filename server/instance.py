import logging
import os
from datetime import datetime
from fastapi import FastAPI
from server.resources import router


log_filename = os.path.join("logs", f"api_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("API service started.")

app = FastAPI(
    title="Podcast text generator",
    description="Audio-podcast creation service using ChatGPT"
)

app.include_router(router=router)
