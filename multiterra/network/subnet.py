import pulumi
import pulumi_aws as aws

from ..generalized_cr import GeneralizedCR

class GeneralizedSubnet(GeneralizedCR):
    def __init__(self, name: str, vpc, cidr_block, opts=None):
        super().__init__('custom:resources:GeneralizedSubnet', name, [vpc], opts=opts)
        self.name = name
        self.vpc = vpc
        self.cidr_block = cidr_block

    def _create_aws(self, region: str):
        instance = aws.ec2.Subnet(
            self.name,
            vpc_id=self.vpc.get_instance("aws", region).id,
            cidr_block=self.cidr_block,
            opts = pulumi.ResourceOptions(parent=self),
        )
        self.register_outputs({"aws_subnet_id": instance.id}) # try to keep common output format
        return instance
