from constructs import Construct
from aws_cdk import (
    Stage
)
from player_lambda.infrastructure.delete_player_event_stack import DeletePlayerEventHandlerStack


class DeletePlayerEventHandlerStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = DeletePlayerEventHandlerStack(self, 'DeletePlayerEventHandlerStack')
