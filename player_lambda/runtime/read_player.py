import json
import datetime

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service="ReadPlayer")


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> str:
    logger.info({'request': event})
    logger.info('PlayerApi kicked off from Player EventBridge in Compute')
