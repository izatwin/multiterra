from __future__ import annotations

from typing import Optional, TypedDict

import pulumi
import pulumi_aws as aws

from ..generalized_cr import DeploymentState, GeneralizedCR


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

    def _create_aws(self, deployment: DeploymentState, region: str) -> aws.ec2.Subnet:
        provider = deployment.get_provider("aws", region, self)
        vpc = self.vpc.get_instance(deployment, "aws", region)
        instance = aws.ec2.Subnet(
            self.resource_name_prefix("aws", region),
            vpc_id=vpc.id,
            cidr_block=self.cidr_block,
            opts=pulumi.ResourceOptions(parent=self, provider=provider),
        )
        return instance
