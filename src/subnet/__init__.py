import pulumi
import pulumi_aws as aws

class GeneralizedSubnet(pulumi.ComponentResource):
    def __init__(self, name: str, vpc, cidr_block, opts=None):
        super().__init__('custom:resources:GeneralizedSubnet', name, opts=opts)
        self.instance = dict()
        self.name = name
        self.vpc = vpc
        self.cidr_block = cidr_block

    def set_providers(self, providers: List[str]):
        self.vpc.set_providers(providers)
        for p in providers:
            if p in self.instance:
                continue
            if p == "aws":
                self.instance["aws"] = aws.ec2.Subnet(
                    self.name,
                    vpc_id=self.vpc.instance["aws"].id,
                    cidr_block=self.cidr_block,
                    opts = pulumi.ResourceOptions(parent=self),
                )
                self.register_outputs({"aws_subnet_id": self.instance["aws"].id}) # try to keep common output format
            else:
                raise ValueError("Provider not implemented")
