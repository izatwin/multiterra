from __future__ import annotations

from typing import NotRequired, Optional, TypedDict, cast

import pulumi

from ..generalized_cr import Deployment, GeneralizedCR
from .utilsAwsVM import config_aws, createVM_AWS


class GeneralizedVMArgs(TypedDict):
    tier: str
    subnet: GeneralizedCR
    image: NotRequired[GeneralizedCR]


class GeneralizedVM(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedVMArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        deps = [args["subnet"]]
        image = args.get("image")
        if image is not None:
            deps.append(image)

        super().__init__("multiterra:vm:GeneralizedVM", name, deps, opts=opts)
        self.subnet = args["subnet"]
        self.tier = cast(str, args["tier"])
        self.image = image

    def _create_aws(self, deployment: Deployment, region: str):
        provider = deployment.get_deployment_provider("aws", region)
        subnet = self.subnet.get_instance(deployment, "aws", region)
        image = None if self.image is None else self.image.get_instance(deployment, "aws", region)
        return createVM_AWS(
            deployment,
            self.resource_name_prefix("aws", region),
            config_aws[self.tier],
            subnet,
            provider,
            image,
        )
