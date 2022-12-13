import json
import datetime
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service="ReadPlayer")


dynamodb = boto3.resource('dynamodb')


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> str:
    logger.info({'request': event})
    logger.info('ReadPlayer kicked off from Player EventBridge in Compute')

    table = dynamodb.Table(
        'DeployPlayerDynamoDB-PlayerDynamoDBStack-TGL768AF672-I9YBTMG19E08')

    response = table.scan()

    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data
