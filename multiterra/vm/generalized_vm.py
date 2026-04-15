from __future__ import annotations

from typing import NotRequired, Optional, TypedDict, cast

import pulumi

from ..generalized_cr import DeploymentState, GeneralizedCR
from .utilsAwsVM import config_aws, createVM_AWS


class GeneralizedVMArgs(TypedDict):
    tier: str
    subnet: GeneralizedCR
    image: NotRequired[GeneralizedCR]
    firewalls: NotRequired[list[GeneralizedCR]]


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
        firewalls = args.get("firewalls")
        if firewalls is not None:
            deps.extend(firewalls)

        super().__init__("multiterra:vm:GeneralizedVM", name, deps, opts=opts)
        self.subnet = args["subnet"]
        self.tier = cast(str, args["tier"])
        self.image = image
        self.firewalls = firewalls

    def _create_aws(self, deployment: DeploymentState, region: str):
        provider = deployment.get_provider("aws", region, self)
        subnet = self.subnet.get_instance(deployment, "aws", region)
        image = None if self.image is None else self.image.get_instance(deployment, "aws", region)
        firewalls = None if self.firewalls is None else [f.get_instance(deployment, "aws", region) for f in self.firewalls]
        return createVM_AWS(
            self,
            self.resource_name_prefix("aws", region),
            config_aws[self.tier],
            subnet,
            provider,
            firewalls,
            image,
        )
