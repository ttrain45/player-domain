from constructs import Construct
from aws_cdk import (
    Stage
)
from player_lambda.infrastructure.player_changed_event_stack import PlayerChangedEventStack


class PlayerChangedEventStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = PlayerChangedEventStack(self, 'PlayerChangedEventStack')
