from constructs import Construct
from aws_cdk import (
    Stage
)
from event_bridge.infrastructure.player_event_bridge_stack import PlayerEventBridgeStack


class PlayerEventBridgeStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = PlayerEventBridgeStack(
            self, 'PlayerEventBridge')
