from typing import Optional, TypedDict, cast

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp

from ..generalized_cr import Deployment, GeneralizedCR


class GeneralizedVPCArgs(TypedDict):
    cidr_block: str


class GeneralizedVPC(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedVPCArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__("multiterra:network:GeneralizedVPC", name, [], opts=opts)
        self.cidr_block = args["cidr_block"]

    def _create_aws(
        self, deployment: Deployment, region: str, zone: str
    ) -> aws.ec2.Vpc:
        provider = deployment.get_deployment_provider("aws", region, zone)
        instance = aws.ec2.Vpc(
            self.resource_name_prefix("aws", region),
            cidr_block=self.cidr_block,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        self.gateway = aws.ec2.InternetGateway(
            f"{self.resource_name_prefix('aws', region)}-Gateway",
            vpc_id=instance.id,
            opts=pulumi.ResourceOptions(parent=instance, provider=provider),
        )

        self.route_table = aws.ec2.RouteTable(
            f"{self.resource_name_prefix('aws', region)}-RouteTable",
            vpc_id=instance.id,
            routes=[
                {
                    "cidr_block": "0.0.0.0/0",
                    "gateway_id": self.gateway.id,
                },
            ],
            opts=pulumi.ResourceOptions(parent=instance, provider=provider),
        )


        return instance

    def _create_gcp(self, deployment: Deployment, region: str, zone:str) -> gcp.compute.Network:
        provider = deployment.get_deployment_provider("gcp", region, zone)

        instance = gcp.compute.Network(
            self.resource_name_prefix("gcp", region),
            auto_create_subnetworks=False,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        return instance