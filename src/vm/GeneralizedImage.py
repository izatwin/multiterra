import pulumi
import pulumi_aws as aws


class GeneralizedImage(pulumi.ComponentResource):
    def __init__(self, name: str, image_blob=None, opts=None):
        super().__init__('custom:resources:GeneralizedImage', name, opts=opts)
        self.name = name
        self.image_blob = image_blob
        self.instance = dict()

    def set_providers(self, providers: List[str]):
        for p in providers:
            if p in self.instance:
                continue
            if p ==  "aws":
                self.instance["aws"] = aws.ec2.get_ami(
                    most_recent=True,
                    owners=["137112412989"],
                    filters=[{
                        "name": "name",
                        "values": ["amzn2-ami-hvm-*-x86_64-gp2"]
                    }]
                )
            else:
                raise ValueError("Provider not implemented")






