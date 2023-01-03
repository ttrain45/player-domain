from constructs import Construct
from aws_cdk import (
    Stack,
    pipelines as pipelines,
    SecretValue
)

from player_lambda.infrastructure.add_player_event_stage import AddPlayerEventStage
from player_lambda.infrastructure.edit_player_event_stage import EditPlayerEventHandlerStage
from player_lambda.infrastructure.delete_player_event_stage import DeletePlayerEventHandlerStage
from event_bridge.infrastructure.player_event_bridge_stage import PlayerEventBridgeStage


class PipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        code_pipeline = pipelines.CodePipeline(
            self,
            'Player-Pipeline',
            docker_enabled_for_synth=True,
            synth=pipelines.ShellStep('Synth',
                                      input=pipelines.CodePipelineSource.git_hub(
                                          'ttrain45/player-domain',
                                          'feature/rest-lambda-integration',
                                          authentication=SecretValue.secrets_manager(
                                              'exploration-token')
                                      ),
                                      env={'privileged': 'True'},
                                      commands=[
                                          "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                                          # Instructs Codebuild to install required packages
                                          "pip3 install -r requirements.txt",
                                          "cdk synth"
                                      ]
                                      )
        )

        deploy_add_player_event = AddPlayerEventStage(
            self, "DeployAddPlayerEvent")
        deploy_add_player_event_stage = code_pipeline.add_stage(
            deploy_add_player_event)

        deploy_edit_player_event = EditPlayerEventHandlerStage(
            self, "DeployEditPlayerEvent")
        deploy_add_player_event_stage = code_pipeline.add_stage(
            deploy_edit_player_event)

        deploy_delete_player_event = DeletePlayerEventHandlerStage(
            self, "DeployDeletePlayerEvent")
        deploy_delete_player_event_stage = code_pipeline.add_stage(
            deploy_delete_player_event)

        deploy_player_event_bridge = PlayerEventBridgeStage(
            self, "DeployPlayerEventBridge")
        deploy_player_event_bridge_stage = code_pipeline.add_stage(
            deploy_player_event_bridge)
