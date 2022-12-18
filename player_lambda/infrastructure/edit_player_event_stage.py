from constructs import Construct
from aws_cdk import (
    Stage
)
from player_lambda.infrastructure.edit_player_event_stack import EditPlayerEventHandlerStack


class EditPlayerEventHandlerStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = EditPlayerEventHandlerStack(self, 'EditPlayerEventHandlerStack')
