from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as python,
    aws_s3 as s3,
    aws_dynamodb as dynamodb
)
from constructs import Construct


class EditPlayerEventStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### Create Edit Player Lambda ###
        edit_player_event = python.PythonFunction(self, "EditPlayer",
                                                    entry="player_lambda/runtime",  # required
                                                    runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                                    index="edit_player_event.py",  # optional, defaults to 'index.py'
                                                    handler="handler",
                                                    memory_size=256,
                                                    function_name="EditPlayer"
                                                    )

        ### Update and grant invoke Lambda permission to this lambda ###
        ### from event bridge events ###
        principal = iam.ServicePrincipal("events.amazonaws.com")
        edit_player_event.grant_invoke(principal)

        ### Get PlayerS3BucketData reference ###
        player_s3_bucket = s3.Bucket.from_bucket_name(
            self,
            "event-driven-exploration-player-bucket-1029",
            "event-driven-exploration-player-bucket-1029"
        )

        dynamodb_table = dynamodb.Table.from_table_name(
            self,
            "TGL",
            "TGL")

        dynamodb_table.grant_read_write_data(edit_player_event)

        ### Update and grant invoke Lambda permission to this lambda ###
        ### from event bridge events ###
        # change_player_event.grant_invoke(player_s3_bucket)
