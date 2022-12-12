from constructs import Construct
from aws_cdk import (
    Stage
)
from player_lambda.infrastructure.add_player_event_stack import AddPlayerEventStack


class AddPlayerEventStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = AddPlayerEventStack(self, 'AddPlayerEventStack')
