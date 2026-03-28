# ---------------
#     Imports
# ---------------

import pulumi
import pulumi_aws as aws



# ----------------------------
#     AWS Helper Functions
# ----------------------------

def obtainConfig_AWS(self, tier: str):
    config = {}

    match (tier):
        case "high":
            config["instance_type"] = ...
            config["vpc_cidr"] = ...
            config["opts"] = ...
        case "medium":
            config["instance_type"] = ... #"t3.medium"
            config["vpc_cidr"] = ... #"10.0.0.0/16"
            config["opts"] = ...
        case "low":
            config["instance_type"] = ... #"t3.micro"
            config["vpc_cidr"] = ... #"10.0.0.0/16"
            config["opts"] = ...
        case _:
            config["instance_type"] = ...
            config["vpc_cidr"] = ...
            config["opts"] = ...

    return config


def createVM_AWS(self, name: str, config: str):
    # Create VPC
    vpc = aws.ec2.Vpc(
        f"{name}-vpc",
        cidr_block = config["vpc_cidr"],
        opts = pulumi.ResourceOptions(parent=self)
    )

    # Get latest Amazon Linux AMI
    ami = aws.get_ami(
        filters = [{"name": "name", "values": ["amzn2-ami-hvm-*-x86_64-gp2"]}],
        owners = ["137112412989"],
        most_recent = True
    )

    # Create EC2 instance
    instance = aws.ec2.Instance(
        f"{name}-instance",
        instance_type = config["instance_type"],
        ami = ami.id,
        subnet_id = vpc.id,  # simplified
        opts = pulumi.ResourceOptions(parent=self)
    )

    return instance