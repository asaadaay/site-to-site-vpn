vpc_config = [
    {"name": "cloud-network", "cidr": "10.0.0.0/20"},
    {"name": "on-prem-network", "cidr": "10.0.16.0/20"}
]

subnets_config = [
    {"name": "private", "type": "PRIVATE_WITH_NAT"},
    {"name": "public", "type": "PUBLIC"}
]

ec2_config = [
    {
        "name": f"{vpc_config[0]["name"]}-server",
        "vpc": vpc_config[0]["name"],
        "instance-type": "t2.micro",
        "subnet-type": "PRIVATE_WITH_NAT"
    },
    {
        "name": f"{vpc_config[1]["name"]}-server",
        "vpc": vpc_config[1]["name"],
        "instance-type": "t2.micro",
        "subnet-type": "PRIVATE_WITH_NAT"
    },
    {
        "name": f"{vpc_config[1]["name"]}-router",
        "vpc": vpc_config[1]["name"],
        "instance-type": "t2.micro",
        "subnet-type": "PUBLIC"
    }
]