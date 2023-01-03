import json
import datetime
import boto3

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

client = boto3.client('events')

logger = Logger(service="EditPlayerEvent")

tracer = Tracer(service="EditPlayerEvent")

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> str:
    logger.info(event["detail"])
    tracer.put_annotation(key="EventId", value='test value')

    edit_player_payload = json.loads(event.get("detail", {}).get("body"))

    edit_player_event_entries = [
        {
            'Source': 'editPlayerEvent',
            'DetailType': 'EditPlayer',
            'Detail': json.dumps(edit_player_payload),
            'EventBusName': 'PlayerDataEventBus'
        },
    ]

    logger.info({'edit_player_event': edit_player_event_entries})

    edit_player_response = client.put_events(
        Entries=edit_player_event_entries
    )

    logger.info(edit_player_response)

    logger.info('EditPlayerEvent kicked off from Player EventBridge')
