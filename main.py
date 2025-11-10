# @author: Panado (yesdotcom), 2025

import asyncio
import json
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from tortoise import Tortoise

from utils.security_tools import Verify
from utils.SQL_tools import DatabaseOperations

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()


@app.post("/add_record")
async def add_record(request: Request):
    logger.info("Raw body received for add_record endpoint.")
    raw_body = await request.body()
    try:
        verifier = Verify()
        verifier.verify_received_request(request=request, body=raw_body)
    except HTTPException as e:
        logger.error(f"Signature verification failed: {e.detail}")
        raise e
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    logger.info(f"Data received: {data}")

    # Execute instructions of request in background
    asyncio.create_task(DatabaseOperations.add_item(data=data))

    logger.info("OK")

    return {"status": 200}


@app.get("/health")
def health():
    logger.info("Health check endpoint called.")
    return {"status": "OK"}


async def init_tortoise():
    uri = os.getenv("PG_URI")
    await Tortoise.init(
        db_url=uri,
        modules={"models": ["utils.SQL_tools"]},
    )
    await Tortoise.generate_schemas()
    logger.info("Tortoise ORM initialized and schemas generated.")


@app.on_event("startup")
async def startup_event():
    await init_tortoise()
