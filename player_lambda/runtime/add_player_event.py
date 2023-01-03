import json
import datetime
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

client = boto3.client('events')

logger = Logger(service="AddPlayerEvent")


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> str:
    logger.info(event["detail"])

    detail_dict = json.loads(event.get("detail", {}).get("body"))

    add_player_default_add_ons = {"validated": "true", "status": "active",
                                  "pgatStatus": "active", "injuriedReserve": "false", "eligible": "true"}

    add_player_event_data_with_defaults = {
        **detail_dict, **add_player_default_add_ons}

    save_player_event_entries = [
        {
            'Source': 'addPlayerEvent',
            'DetailType': 'SavePlayer',
            'Detail': json.dumps(add_player_event_data_with_defaults),
            'EventBusName': 'PlayerDataEventBus'
        },
    ]

    logger.info({'save_player_event': save_player_event_entries})

    save_player_response = client.put_events(
        Entries=save_player_event_entries
    )

    logger.info('AddPlayerEvent kicked off from Player EventBridge')
