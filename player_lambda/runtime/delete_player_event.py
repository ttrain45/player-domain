import json
import datetime
import boto3

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

client = boto3.client('events')

logger = Logger(service="DeletePlayerEvent")

tracer = Tracer(service="DeletePlayerEvent")

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> str:
    logger.info(event["detail"])
    tracer.put_annotation(key="EventId", value='test value')

    delete_player_payload = event.get("detail")

    delete_player_payload["eventName"] = "DeletePlayer"

    delete_player_event_entries = [
        {
            'Source': 'deletePlayerEvent',
            'DetailType': 'player',
            'Detail': json.dumps(delete_player_payload),
            'EventBusName': 'PlayerDataEventBus'
        },
    ]

    logger.info({'delete_player_event': delete_player_event_entries})

    delete_player_response = client.put_events(
        Entries=delete_player_event_entries
    )

    logger.info(delete_player_response)

    logger.info('DeletePlayerEvent kicked off from Player EventBridge')
