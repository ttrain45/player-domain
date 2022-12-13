import json
import datetime
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service="SavePlayerEvent")


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> str:
    logger.info({'request': event})
    logger.info({'detail': event.detail})
    logger.info('SavePlayerEvent kicked off from Player EventBridge')
