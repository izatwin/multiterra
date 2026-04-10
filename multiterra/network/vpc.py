import pulumi
import pulumi_aws as aws

from ..generalized_cr import GeneralizedCR

class GeneralizedVPC(GeneralizedCR):
    def __init__(self, name: str, cidr_block, opts=None):
        super().__init__('custom:resources:GeneralizedVPC', name, [], opts=opts)
        self.name = name
        self.cidr_block = cidr_block

    def _create_aws(self, deployment, region: str):
        instance = aws.ec2.Vpc(
            self.name,
            cidr_block=self.cidr_block,
            opts = pulumi.ResourceOptions(parent=self),
        )
        self.register_outputs({"aws_vpc_id": instance.id}) # try to keep common output format
        return instance
