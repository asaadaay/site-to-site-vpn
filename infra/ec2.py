from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Fn
)
from constructs import Construct

from infra.config import ec2_config

class EC2(Construct):
    def __init__(self, scope: Construct, construct_id: str, stack_name, vpcs, elastic_ip, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        userdata = open("infra/user_data.sh").read()

        ec2_role = iam.Role(
                self, 
                f"{stack_name}-ec2-role",
                role_name=f"{stack_name}-ec2-role",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                ]
            )

        self.instances = {}
        for instance in ec2_config:
            instance_sg = ec2.SecurityGroup(
                self,
                f"{stack_name}-{instance["name"]}-sg",
                vpc=vpcs[instance["vpc"]],
                security_group_name=f"{stack_name}-{instance["name"]}-sg"
            )
            instance_sg.add_ingress_rule(
                ec2.Peer.any_ipv4(),
                ec2.Port.all_traffic(),
                "Allow all traffic"
            )

            if instance["name"] == ec2_config[2]["name"]:
                userdata = open("infra/user_data.sh").read()
                userdata = ec2.UserData.custom(userdata)
            else:
                userdata = None

            ec2_instance = ec2.Instance(
                self,
                f"{stack_name}-{instance["name"]}",
                instance_type=ec2.InstanceType(instance["instance-type"]),
                machine_image=ec2.MachineImage.generic_linux(
                    ami_map={
                        "us-east-1": "ami-020cba7c55df1f615"
                    }
                ),
                vpc=vpcs[instance["vpc"]],
                instance_name=f"{stack_name}-{instance["name"]}",
                role=ec2_role,
                security_group=instance_sg,
                vpc_subnets=ec2.SubnetSelection(subnet_type=getattr(ec2.SubnetType, instance["subnet-type"])),
                user_data=userdata
            )
            self.instances[instance["name"]] = ec2_instance


        ec2.CfnEIPAssociation(
            self,
            "eip-association",
            instance_id=self.instances[ec2_config[2]["name"]].instance_id,
            allocation_id=elastic_ip.attr_allocation_id
        )