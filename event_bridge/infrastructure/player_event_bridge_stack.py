from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    aws_events as events,
    aws_events_targets as target,
    aws_iam as iam,
    aws_lambda_python_alpha as python
)


class PlayerEventBridgeStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ### Create Player Event Bus ###
        player_event_bus = events.EventBus(self,
                                           id='player-event-bus',
                                           event_bus_name='PlayerEventBus'
                                           )

        ### Create Player Event Bus Archive ###
        player_event_bus.archive('PlayerEventBusArchive',
                                 archive_name='PlayerEventBusArchive',
                                 description='PlayerEventBus Archive',
                                 event_pattern=events.EventPattern(
                                     account=[Stack.of(self).account]
                                 ),
                                 retention=Duration.days(1)
                                 )

        ### Creating Change Player Rule in Infrastructure, not sure if this ###
        ### should live somewhere else in the package structure ###
        change_player_rule = events.Rule(self, "change-player-rule",
                                         event_bus=player_event_bus,
                                         event_pattern=events.EventPattern(
                                             detail_type=["player"],
                                             detail={
                                                 "eventName": ["ChangePlayerName"]
                                             },
                                         )
                                         )

        ### Get Player Api Lambda previously created ###
        player_api = python.PythonFunction.from_function_name(
            self, "ChangePlayerEvent", "ChangePlayerEvent")

        ### Add Player Api Lambda as a target for the change team rule ###
        change_player_rule.add_target(
            target.LambdaFunction(
                player_api
            ))

        add_player_rule = events.Rule(self, "add-player-rule",
                                      event_bus=player_event_bus,
                                      event_pattern=events.EventPattern(
                                            detail_type=["player"],
                                            detail={
                                                "eventName": ["AddPlayer"]
                                            },
                                      )
                                      )

        add_player_lambda = python.PythonFunction.from_function_name(
            self, "AddPlayerEventHandler", "AddPlayerEventHandler")

        add_player_rule.add_target(
            target.LambdaFunction(
                add_player_lambda
            ))

        edit_player_rule = events.Rule(self, "edit-player-event-rule",
                                      event_bus=player_event_bus,
                                      event_pattern=events.EventPattern(
                                            detail_type=["player"],
                                            detail={
                                                "eventName": ["EditPlayer"]
                                            },
                                      )
                                      )

        edit_player_lambda = python.PythonFunction.from_function_name(
            self, "EditPlayerEvent", "EditPlayerEvent")

        edit_player_rule.add_target(
            target.LambdaFunction(
                edit_player_lambda
            ))
