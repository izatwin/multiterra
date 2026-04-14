from typing import Optional, TypedDict, cast

import pulumi
import pulumi_aws as aws

from ..generalized_cr import Deployment, GeneralizedCR


class GeneralizedImageArgs(TypedDict):
    image_blob: str


class GeneralizedImage(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedImageArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("multiterra:vm:GeneralizedImage", name, [], opts=opts)
        self.image_blob = args["image_blob"]

    def _create_aws(self, deployment: Deployment, region: str) -> aws.ec2.GetAmiResult:
        provider = deployment.get_deployment_provider("aws", region)
        return aws.ec2.get_ami(
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
