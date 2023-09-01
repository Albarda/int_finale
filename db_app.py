from aws_cdk import (
    core as cdk,
    aws_ecs as ecs,
    aws_ecr as ecr
)
#test-11
from aws_solutions_constructs.aws_fargate_dynamodb import FargateToDynamoDB, FargateToDynamoDBProps

class MyFargateStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Existing ECR repository
        ecr_repository = ecr.Repository.from_repository_arn(
            self, 'ExistingEcrRepo',
            "704059047372.dkr.ecr.eu-west-1.amazonaws.com/db_app:latest"
        )

        # ECS Task Definition with the existing ECR repository
        task_definition = ecs.FargateTaskDefinition(
            self, 'int_final'
        )
        container = task_definition.add_container(
            'MyContainer',
            image=ecs.ContainerImage.from_ecr_repository(ecr_repository)
        )

        # Create Fargate Service and DynamoDB table
        FargateToDynamoDB(self, 'FargateToDynamoDB',
            public_api=True,
            fargate_task_definition=task_definition
        )

