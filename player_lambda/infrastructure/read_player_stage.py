from constructs import Construct
from aws_cdk import (
    Stage
)
from player_lambda.infrastructure.read_player_stack import ReadPlayerStack


class ReadPlayerStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = ReadPlayerStack(self, 'ReadPlayerStack')
