from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as python,
    aws_dynamodb as dynamodb
)
from constructs import Construct


class ReadPlayerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### Read Player Lambda ###
        read_player = python.PythonFunction(self, "ReadPlayer",
                                            entry="player_lambda/runtime",  # required
                                            runtime=_lambda.Runtime.PYTHON_3_8,  # required
                                            index="read_player.py",  # optional, defaults to 'index.py'
                                            handler="handler",
                                            memory_size=256,
                                            function_name="ReadPlayer"
                                            )
        ### Update and grant invoke Lambda permission to this lambda ###
        ### from event bridge events ###
        principal = iam.ServicePrincipal("apigateway.amazonaws.com")
        read_player.grant_invoke(principal)

        read_player.add_function_url()

        dynamodb_table = dynamodb.Table.from_table_name(
            self,
            "DeployPlayerDynamoDB-PlayerDynamoDBStack-TGL768AF672-I9YBTMG19E08",
            "DeployPlayerDynamoDB-PlayerDynamoDBStack-TGL768AF672-I9YBTMG19E08")

        dynamodb_table.grant_read_data(read_player)
