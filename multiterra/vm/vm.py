from __future__ import annotations

from typing import NotRequired, Optional, TypedDict, cast

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp

from ..generalized_cr import Deployment, GeneralizedCR


config_aws = {
    "high": {
        "instance_type": "t3.large",
    },
    "medium": {
        "instance_type": "t3.medium",
    },
    "low": {
        "instance_type": "t3.micro",
    },
}


config_gcp = {
    "high": {
        "machine_type": "e2-standard-4",
    },
    "medium": {
        "machine_type": "e2-standard-2",
    },
    "low": {
        "machine_type": "e2-micro",
    },
}


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


    def _create_aws(self, deployment: Deployment, region: str, zone:str):
        name = self.resource_name_prefix("aws", region)
        config = config_aws[self.tier]
        provider = deployment.get_deployment_provider("aws", region, zone)
        subnet = self.subnet.get_instance(deployment, "aws", region)
    
        if self.image is None: 
            image = aws.ec2.get_ami(
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
        else:
            image = self.image.get_instance(deployment, "aws", region)    

        return aws.ec2.Instance(
            f"{name}-instance",
            instance_type=config["instance_type"],
            ami=image.id,
            subnet_id=subnet.id,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )


    def _create_gcp(self, deployment: Deployment, region: str, zone:str):
        name = self.resource_name_prefix("gcp", region).lower()
        config = config_gcp[self.tier]
        provider = deployment.get_deployment_provider("gcp", region, zone)
        subnet = self.subnet.get_instance(deployment, "gcp", region)

        if self.image is None: 
            image = gcp.compute.get_image(
                family="debian-11",
                project="debian-cloud",
                opts=pulumi.InvokeOptions(provider=provider),
            )
        else:
            image = self.image.get_instance(deployment, "gcp", region)

        return gcp.compute.Instance(
            f"{name}-instance",
            machine_type=config["machine_type"],
            zone=zone,

            boot_disk={
                "initialize_params": {
                    "image": image.self_link,
                }
            },

            network_interfaces=[{
                "subnetwork": subnet.id,
                "access_configs": [{}],
            }],

            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )