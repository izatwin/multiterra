from __future__ import annotations

from typing import Optional, TypedDict

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp

from ..generalized_cr import Deployment, GeneralizedCR


class GeneralizedSubnetArgs(TypedDict):
    vpc: GeneralizedCR
    cidr_block: str


class GeneralizedSubnet(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedSubnetArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        super().__init__(
            "multiterra:network:GeneralizedSubnet",
            name,
            [args["vpc"]],
            opts=opts,
        )
        self.vpc = args["vpc"]
        self.cidr_block = args["cidr_block"]

    def _create_aws(
        self, deployment: Deployment, region: str, zone: str
    ) -> aws.ec2.Subnet:
        name = self.resource_name_prefix("aws", region, zone).lower().replace("_", "-")
        provider = deployment.get_deployment_provider("aws", region, zone)
        vpc = self.vpc.get_instance(deployment, "aws", region, zone)
        instance = aws.ec2.Subnet(
            name,
            vpc_id=vpc.id,
            cidr_block=self.cidr_block,
            availability_zone=zone,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        vpc_route_table = self.vpc.get_extra(deployment, "route_table", "aws", region, zone)

        route_table_association = aws.ec2.RouteTableAssociation(
            f"{name}-association",
            subnet_id=instance.id,
            route_table_id=vpc_route_table.id,
            opts=pulumi.ResourceOptions(parent=instance, provider=provider),
        )

        return instance


    def _create_gcp(self, deployment: Deployment, region: str, zone:str) -> gcp.compute.Subnetwork:
        name = self.resource_name_prefix("gcp", region, zone).lower().replace("_", "-")
        provider = deployment.get_deployment_provider("gcp", region, zone)

        vpc = self.vpc.get_instance(deployment, "gcp", region, zone)

        instance = gcp.compute.Subnetwork(
            name,
            ip_cidr_range=self.cidr_block,
            region=region,
            network=vpc.id,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        return instance