from enum import Enum, auto
from typing import NotRequired, Optional, TypedDict

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp

from ..generalized_cr import Deployment, GeneralizedCR


class ImageEnum(Enum):
    UBUNTU = auto()
    DEBIAN = auto()


class GeneralizedImageArgs(TypedDict):
    image_name: ImageEnum
    user_data: NotRequired[str | pulumi.Output[str]]


class GeneralizedImage(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedImageArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("multiterra:vm:GeneralizedImage", name, [], opts=opts)
        self.image_name = args["image_name"]
        self.user_data = args.get("user_data")

    def _create_aws(
        self, deployment: Deployment, region: str, zone: str
    ) -> aws.ec2.GetAmiResult:
        provider = deployment.get_deployment_provider("aws", region, zone)
        if self.image_name == ImageEnum.UBUNTU:
            return aws.ec2.get_ami(
                most_recent=True,
                owners=["099720109477"],
                filters=[
                    {
                        "name": "name",
                        "values": [
                            "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
                        ],
                    },
                    {
                        "name": "virtualization-type",
                        "values": ["hvm"],
                    },
                ],
                opts=pulumi.InvokeOptions(provider=provider),
            )
        elif self.image_name == ImageEnum.DEBIAN:
            return aws.ec2.get_ami(
                most_recent=True,
                owners=["136693071363"],
                filters=[
                    {
                        "name": "name",
                        "values": ["debian-12-amd64-*"],
                    },
                    {
                        "name": "virtualization-type",
                        "values": ["hvm"],
                    },
                ],
                opts=pulumi.InvokeOptions(provider=provider),
            )

        raise ValueError("Unknown Image")

    def _create_gcp(
        self, deployment: Deployment, region: str, zone: str
    ) -> gcp.compute.GetImageResult:
        provider = deployment.get_deployment_provider("gcp", region, zone)
        if self.image_name == ImageEnum.UBUNTU:
            return gcp.compute.get_image(
                most_recent=True,
                family="ubuntu-2204-lts",
                project="ubuntu-os-cloud",
                opts=pulumi.InvokeOptions(provider=provider),
            )
        elif self.image_name == ImageEnum.DEBIAN:
            return gcp.compute.get_image(
                most_recent=True,
                family="debian-12",
                project="debian-cloud",
                opts=pulumi.InvokeOptions(provider=provider),
            )
        raise ValueError("Unknown Image")
