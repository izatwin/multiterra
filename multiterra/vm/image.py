from typing import Optional, TypedDict, cast

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp

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

    def _create_aws(self, deployment: Deployment, region: str, zone:str) -> aws.ec2.GetAmiResult:
        provider = deployment.get_deployment_provider("aws", region, zone)
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
    

    def _create_gcp(self, deployment: Deployment, region: str, zone: str) -> gcp.compute.GetImageResult:
        provider = deployment.get_deployment_provider("gcp", region, zone)
        return gcp.compute.get_image(
            most_recent=True,
            family="ubuntu-2204-lts",
            project="ubuntu-os-cloud",
            opts=pulumi.InvokeOptions(provider=provider),
        )
