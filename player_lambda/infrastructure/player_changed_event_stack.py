from aws_cdk import (
    Stack,
    aws_lambda_python_alpha as python,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3notification
)
from constructs import Construct


class PlayerChangedEventStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### Create PlayerChangeEvent Lambda ###
        player_changed_event = python.PythonFunction(self, "PlayerChangedEvent",
                                                     entry="player_lambda/runtime",  # required
                                                     runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                                     index="player_changed_event.py",  # optional, defaults to 'index.py'
                                                     handler="handler",
                                                     memory_size=256,
                                                     function_name="PlayerChangedEvent"
                                                     )

        ### Get PlayerS3BucketData reference ###
        player_s3_bucket = s3.Bucket.from_bucket_name(
            self,
            "event-driven-exploration-player-bucket-1029",
            "event-driven-exploration-player-bucket-1029"
        )

        ### Add lambda access to s3 bucket ###
        player_s3_bucket.grant_read_write(player_changed_event)

        ### Update and grant invoke Lambda permission to this lambda ###
        ### from event bridge events ###
        # player_changed_event.grant_invoke(player_s3_bucket)

        player_s3_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3notification.LambdaDestination(player_changed_event))
