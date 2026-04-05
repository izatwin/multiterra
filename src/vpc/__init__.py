import pulumi
import pulumi_aws as aws

class GeneralizedVPC(pulumi.ComponentResource):
    def __init__(self, name: str, cidr_block, opts=None):
        super().__init__('custom:resources:GeneralizedVPC', name, opts=opts)
        self.instance = dict()
        self.name = name
        self.cidr_block = cidr_block

    def set_providers(self, providers: List[str]):
        for p in providers:
            if p in self.instance:
                continue
            if p == "aws":
                self.instance["aws"] = aws.ec2.Vpc(
                    self.name,
                    cidr_block=self.cidr_block,
                    opts = pulumi.ResourceOptions(parent=self),
                )
                self.register_outputs({"aws_vpc_id": self.instance["aws"].id}) # try to keep common output format
            else:
                raise ValueError("Provider not implemented")
