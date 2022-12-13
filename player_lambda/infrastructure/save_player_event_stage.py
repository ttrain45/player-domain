from constructs import Construct
from aws_cdk import (
    Stage
)
from player_lambda.infrastructure.save_player_event_stack import SavePlayerEventStack


class SavePlayerEventStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = SavePlayerEventStack(self, 'SavePlayerEventStack')
