import aws_cdk as core
import aws_cdk.assertions as assertions

from player_domain.player_domain_stack import PlayerDomainStack

# example tests. To run these tests, uncomment this file along with the example
# resource in player_domain/player_domain_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PlayerDomainStack(app, "player-domain")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
