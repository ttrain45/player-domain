from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as python,
    aws_s3 as s3
)
from constructs import Construct


class ReadPlayerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### Read Player Lambda ###
        read_player = python.PythonFunction(self, "ReadPlayer",
                                            entry="player_lambda/runtime",  # required
                                            runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                            index="read_player.py",  # optional, defaults to 'index.py'
                                            handler="handler",
                                            memory_size=256,
                                            function_name="ReadPlayer"
                                            )

        ### Get PlayerS3BucketData reference ###
        player_s3_bucket = s3.Bucket.from_bucket_name(
            self,
            "event-driven-exploration-player-bucket-1029",
            "event-driven-exploration-player-bucket-1029"
        )

        ### Add lambda access to s3 bucket ###
        player_s3_bucket.grant_read(read_player)
