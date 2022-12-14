import json
import datetime
import boto3

from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths

logger = Logger(service="ReadPlayer")
tracer = Tracer()
app = APIGatewayHttpResolver()


dynamodb = boto3.resource('dynamodb')


@app.get("/api/player")
@tracer.capture_method
def get_todos():
    #logger.info({'request': event})
    logger.info('ReadPlayer kicked off from Player EventBridge in Compute')

    table = dynamodb.Table(
        'DeployPlayerDynamoDB-PlayerDynamoDBStack-TGL768AF672-I9YBTMG19E08')

    response = table.scan()

    data = response['Items']

    logger.info("Testing")

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    logger.info("Testing...")

    return data


# You can continue to use other utilities just as before
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info(context)
    logger.info(event)
    return app.resolve(event, context)
