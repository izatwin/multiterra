from typing import Optional, TypedDict, cast

import pulumi
import pulumi_aws as aws

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

    def _create_aws(self, deployment: Deployment, region: str) -> aws.ec2.Vpc:
        provider = deployment.get_deployment_provider("aws", region)
        instance = aws.ec2.Vpc(
            self.resource_name_prefix("aws", region),
            cidr_block=self.cidr_block,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )
        return instance
