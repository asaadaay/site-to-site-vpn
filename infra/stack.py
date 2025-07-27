from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from infra.vpc import VPC
from infra.ec2 import EC2

class SiteToSiteVpnStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, stack_name, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_construct = VPC(
            self,
            "vpc-construct",
            stack_name=stack_name
        )

        EC2(
            self,
            "ec2-construct",
            stack_name=stack_name,
            vpcs=vpc_construct.vpcs,
            elastic_ip=vpc_construct.elastic_ip
        )
        



