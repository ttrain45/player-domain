import json
import datetime
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

client = boto3.client('events')

logger = Logger(service="AddPlayerEvent")


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> str:
    logger.info({'request': event})

    logger.info({'detail': event.detail})
    detail_dict = event.detail
    save_player_event_entries = [
        {
            'Source': 'addPlayerEvent',
            'DetailType': 'player',
            'Detail': '{"eventName": "SavePlayer", "firstName": "{first_name}","lastName": "{last_name}", "college": "{college}", "validated": "true","status": "active", "pgatStatus": "active", "putOnIr": "false", "eligible": "true"}'.format(first_name=detail_dict.first_name, last_name=detail_dict.last_name, college=detail_dict.college),
            'EventBusName': 'PlayerEventBus'
        },
    ]

    logger.info({'save_player_event': save_player_event_entries})

    save_player_response = client.put_events(
        Entries=save_player_event_entries
    )

    logger.info('AddPlayerEvent kicked off from Player EventBridge')
