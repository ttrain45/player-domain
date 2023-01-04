import os
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_logs as logs,
    Duration,
    aws_events as events,
    aws_events_targets as target,
    aws_iam as iam,
    RemovalPolicy,
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

        add_player_rule = events.Rule(self, "add-player-rule",
                                      event_bus=player_event_bus,
                                      event_pattern=events.EventPattern(
                                            detail_type=["PLAYER"],
                                            detail={
                                                "httpMethod": ["POST"]
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
                                            detail_type=["PLAYER"],
                                            detail={
                                                "httpMethod": ["PATCH"]
                                            },
                                        )
                                      )

        edit_player_lambda = python.PythonFunction.from_function_name(
            self, "EditPlayerEventHandler", "EditPlayerEventHandler")

        edit_player_rule.add_target(
            target.LambdaFunction(
                edit_player_lambda
            ))

        delete_player_rule = events.Rule(self, "delete-player-event-rule",
                                      event_bus=player_event_bus,
                                      event_pattern=events.EventPattern(
                                            detail_type=["PLAYER"],
                                            detail={
                                                "httpMethod": ["DELETE"]
                                            },
                                        )
                                      )

        delete_player_lambda = python.PythonFunction.from_function_name(
            self, "DeletePlayerEventHandler", "DeletePlayerEventHandler")

        delete_player_rule.add_target(
            target.LambdaFunction(
                delete_player_lambda
            ))

        event_bridge_log_group = logs.LogGroup(
            self, 
            "PlayerEventBridgeLogs",
            removal_policy=RemovalPolicy.DESTROY,
            retention=logs.RetentionDays.ONE_DAY
        )

        logging_rule = events.Rule(
            self,
            "logging_rule",
            event_bus=player_event_bus,
            event_pattern={"account": [Stack.of(self).account]}
            )

        logging_rule.add_target(target.CloudWatchLogGroup(event_bridge_log_group, max_event_age=Duration.days(1)))

        core_event_bus = events.EventBus.from_event_bus_arn(self,
                                               "core-event-bus",
                                               "arn:aws:events:us-east-1:{}:event-bus/CoreEventBus".format(os.getenv(
                                                   'CDK_DEFAULT_ACCOUNT')))

        cross_app_rule = events.Rule(self, "cross-app-rule",
                                      event_bus=core_event_bus,
                                      event_pattern=events.EventPattern(
                                             source=["ingest-api"],
                                             detail_type=["TESTDOMAIN"],
                                        )
                                      )

        cross_app_rule.add_target(target.CloudWatchLogGroup(event_bridge_log_group, max_event_age=Duration.days(1)))
