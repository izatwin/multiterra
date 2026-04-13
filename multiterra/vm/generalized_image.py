import pulumi
import pulumi_aws as aws

from ..generalized_cr import GeneralizedCR


class GeneralizedImage(GeneralizedCR):
    def __init__(self, name: str, image_blob=None, opts=None):
        super().__init__('custom:resources:GeneralizedImage', name, [], opts=opts)
        self.name = name
        self.image_blob = image_blob

    def _create_aws(self, region):
        aws.ec2.get_ami(
            most_recent=True,
            owners=["137112412989"],
            filters=[{
                "name": "name",
                "values": ["amzn2-ami-hvm-*-x86_64-gp2"]
            }]
        )



