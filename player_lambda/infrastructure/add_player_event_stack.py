from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events as events,
    aws_lambda_python_alpha as python,
    aws_s3 as s3
)
from constructs import Construct


class AddPlayerEventStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        powertools_layer = python.PythonLayerVersion.from_layer_version_arn(
            self,
            id="lambda-powertools",
            layer_version_arn=f"arn:aws:lambda:us-east-1:017000801446:layer:AWSLambdaPowertoolsPythonV2:16"
        )

        ### Create Add Player Lambda ###
        add_player_event = python.PythonFunction(self, "AddPlayerEventHandler",
                                                 entry="player_lambda/runtime",  # required
                                                 runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                                 index="add_player_event.py",  # optional, defaults to 'index.py'
                                                 handler="handler",
                                                 memory_size=256,
                                                 function_name="AddPlayerEventHandler",
                                                 layers=[powertools_layer],
                                                 tracing=_lambda.Tracing.ACTIVE
                                                 )

        ### Update and grant invoke Lambda permission to this lambda ###
        ### from event bridge events ###
        principal = iam.ServicePrincipal("events.amazonaws.com")
        add_player_event.grant_invoke(principal)

        ### Retrieve Player Event Bus from event bus name ###
        player_data_event_bus = events.EventBus.from_event_bus_name(
            self, "PlayerDataEventBus", "PlayerDataEventBus")

        ### Grant Add Player Lambda permissions for Player Data Event Bus put events ###
        player_data_event_bus.grant_put_events_to(add_player_event)
