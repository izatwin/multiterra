import pulumi
import pulumi_aws as aws


config_aws = {
    "high": {
        "instance_type": "t3.large",
    },
    "medium": {
        "instance_type": "t3.medium",
    },
    "low": {
        "instance_type": "t3.micro",
    },
}


def createVM_AWS(
    self,
    name: str,
    config: dict,
    subnet,
    provider: pulumi.ProviderResource,
    firewalls,
    ami=None,
):
    if ami is None:
        ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["137112412989"],
            filters=[
                {
                    "name": "name",
                    "values": ["amzn2-ami-hvm-*-x86_64-gp2"],
                }
            ],
            opts=pulumi.InvokeOptions(provider=provider),
        )

    ami_id = ami.id if hasattr(ami, "id") else ami.image_id

    return aws.ec2.Instance(
        f"{name}-instance",
        instance_type=config["instance_type"],
        ami=ami_id,
        subnet_id=subnet.id,
        vpc_security_group_ids=[f.id for f in firewalls] if firewalls is not None else None,
        opts=pulumi.ResourceOptions(parent=self, provider=provider),
    )
