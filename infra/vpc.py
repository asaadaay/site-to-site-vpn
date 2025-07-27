from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from infra.config import vpc_config
from infra.config import subnets_config

class VPC(Construct):
    def __init__(self, scope: Construct, construct_id: str, stack_name, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnet_configs=[]
        for subnet in subnets_config:
            subnet_configs.append(
                ec2.SubnetConfiguration(
                    name=f"{stack_name}-{subnet["name"]}-subnet",
                    subnet_type=getattr(ec2.SubnetType, subnet["type"]),
                    cidr_mask=24
                )
            )
        
        self.vpcs = {}
        for virtual_private_cloud in vpc_config:
            vpc = ec2.Vpc(
                self, 
                f"{stack_name}-{virtual_private_cloud["name"]}",
                cidr=virtual_private_cloud["cidr"], 
                enable_dns_hostnames=True,
                enable_dns_support=True,
                nat_gateways=1,
                max_azs=2,
                subnet_configuration=subnet_configs,
                vpc_name=virtual_private_cloud["name"]
            )
            self.vpcs[virtual_private_cloud["name"]] = vpc

        self.vpcs[vpc_config[0]["name"]].enable_vpn_gateway(
            type="ipsec.1",
            vpn_route_propagation=[
                ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                )
            ]
        )

        self.elastic_ip = ec2.CfnEIP(
            self,
            "elastic-ip"
        )

        ec2.VpnConnection(
            self,
            "site-to-site-vpn-connection",
            vpc=self.vpcs[vpc_config[0]["name"]],
            ip=self.elastic_ip.ref,
            static_routes=[vpc_config[1]["cidr"]]
        )


        