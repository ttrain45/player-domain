import json
import datetime
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

client = boto3.client('events')

logger = Logger(service="EditPlayerEvent")


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> str:
    logger.info(event["detail"])

    edit_player_payload = event.get("detail")

    edit_player_event_entries = [
        {
            'Source': 'editPlayerEvent',
            'DetailType': 'edit-player',
            'Detail': json.dumps(edit_player_payload),
            'EventBusName': 'PlayerDataEventBus'
        },
    ]

    logger.info({'edit_player_event': edit_player_event_entries})

    edit_player_response = client.put_events(
        Entries=edit_player_event_entries
    )

    logging.info(edit_player_response)

    logger.info('EditPlayerEvent kicked off from Player EventBridge')
