# utilsAwsVM.py



# ---------------
#     Imports
# ---------------



import pulumi
import pulumi_aws as aws



# ----------------------------
#     AWS Helper Functions
# ----------------------------



config_aws = {
    "high": {"instance_type": "t3.large",
    },
    "medium": {"instance_type": "t3.medium",
    },
    "low": {"instance_type": "t3.micro",
    }
}


def createVM_AWS(self, name: str, config: dict, subnet, ami=None):
    if (not ami):
        ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["137112412989"],
            filters=[{
                "name": "name",
                "values": ["amzn2-ami-hvm-*-x86_64-gp2"]
            }]
        )

    ami_id = ami.id if hasattr(ami, "id") else ami.image_id

    instance = aws.ec2.Instance(
        f"{name}-instance",
        instance_type = config["instance_type"],
        ami = ami_id,
        subnet_id = subnet.id,
        opts = pulumi.ResourceOptions(parent=self)
    )

    return instance
