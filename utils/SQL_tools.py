import logging
import time

from dotenv import load_dotenv
from tortoise import fields
from tortoise.models import Model

load_dotenv()

logger = logging.getLogger("main.py")


class Items(Model):
    class Meta:
        table = "items"

    id = fields.IntField(pk=True)
    item_name = fields.TextField()
    item_status = fields.CharField(max_length=20)
    created = fields.IntField(null=False)


class DatabaseOperations:
    @staticmethod
    async def add_item(data: dict):
        logger.info("Creating record for item...")
        await Items.create(
            item_name=data["item"]["name"],
            item_status=data["item"]["status"],
            created=int(time.time()),
        )
