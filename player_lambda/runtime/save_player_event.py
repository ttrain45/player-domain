import json
import datetime
import boto3
import uuid

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service="SavePlayerEvent")


dynamodb = boto3.resource('dynamodb')


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> str:
    logger.info({'request': event})

    detail_dict = event.get("detail")

    detail_dict["id"] = str(uuid.uuid4())

    table = dynamodb.Table(
        'DeployPlayerDynamoDB-PlayerDynamoDBStack-TGL768AF672-I9YBTMG19E08')

    table.put_item(Item=detail_dict)
    logger.info('SavePlayerEvent kicked off from Player EventBridge')
