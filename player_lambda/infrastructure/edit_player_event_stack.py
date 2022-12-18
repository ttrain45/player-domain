from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events as events,
    aws_lambda_python_alpha as python,
    aws_s3 as s3,
    aws_dynamodb as dynamodb
)
from constructs import Construct


class EditPlayerEventStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### Create Edit Player Lambda ###
        edit_player_event = python.PythonFunction(self, "EditPlayerEventHandler",
                                                    entry="player_lambda/runtime",  # required
                                                    runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                                    index="edit_player_event.py",  # optional, defaults to 'index.py'
                                                    handler="handler",
                                                    memory_size=256,
                                                    function_name="EditPlayerEventHandler"
                                                    )

        ### Update and grant invoke Lambda permission to this lambda ###
        ### from event bridge events ###
        principal = iam.ServicePrincipal("events.amazonaws.com")
        edit_player_event.grant_invoke(principal)

        ### Retrieve Player Event Bus from event bus name ###
        player_data_event_bus = events.EventBus.from_event_bus_name(
            self, "PlayerDataEventBus", "PlayerDataEventBus")

        ### Grant Add Player Lambda permissions for Player Data Event Bus put events ###
        player_data_event_bus.grant_put_events_to(edit_player_event)
