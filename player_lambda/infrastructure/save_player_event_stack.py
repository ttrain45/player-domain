from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as python,
    aws_s3 as s3,
    aws_dynamodb as dynamodb
)
from constructs import Construct


class SavePlayerEventStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### Save Add Player Lambda ###
        save_player_event = python.PythonFunction(self, "SavePlayerEvent",
                                                  entry="player_lambda/runtime",  # required
                                                  runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                                  index="save_player_event.py",  # optional, defaults to 'index.py'
                                                  handler="handler",
                                                  memory_size=256,
                                                  function_name="SavePlayerEvent"
                                                  )

        ### Update and grant invoke Lambda permission to this lambda ###
        ### from event bridge events ###
        principal = iam.ServicePrincipal("events.amazonaws.com")
        save_player_event.grant_invoke(principal)

        dynamodb_table = dynamodb.Table.from_table_name(
            self,
            "TGL",
            "TGL")

        dynamodb_table.grant_read_write_data(save_player_event)
