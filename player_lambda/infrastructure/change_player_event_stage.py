from constructs import Construct
from aws_cdk import (
    Stage
)
from player_lambda.infrastructure.change_player_event_stack import ChangePlayerEventStack


class ChangePlayerEventStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = ChangePlayerEventStack(self, 'ChangePlayerEventStack')
