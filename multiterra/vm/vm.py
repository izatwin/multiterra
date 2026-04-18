from __future__ import annotations

from typing import NotRequired, Optional, TypedDict, cast

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp
import pulumi_command as command
from pulumi import FileAsset

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
    firewall: NotRequired[GeneralizedCR]


class GeneralizedVM(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedVMArgs,
        ssh_key=None,
        ssh_user=None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        deps = [args["subnet"]]
        image = args.get("image")
        if image is not None:
            deps.append(image)
        firewall = args.get("firewall")
        if firewall is not None:
            deps.append(firewall)

        super().__init__("multiterra:vm:GeneralizedVM", name, deps, opts=opts)
        self.subnet = args["subnet"]
        self.tier = cast(str, args["tier"])
        self.image = image
        self.firewall = firewall
        self.ssh_key = ssh_key
        self.ssh_user = ssh_user
        self.aws_key_pair = None


    def _create_aws(self, deployment: Deployment, region: str, zone:str):
        name = self.resource_name_prefix("aws", region)
        config = config_aws[self.tier]
        provider = deployment.get_deployment_provider("aws", region, zone)
        subnet = self.subnet.get_instance(deployment, "aws", region)
        firewall = None if self.firewall is None else self.firewall.get_instance(deployment, "aws", region)

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

        if (self.ssh_key is not None) and (self.aws_key_pair is None):
            self.aws_key_pair = aws.ec2.KeyPair(
                f"{self.name}-keypair",
                public_key=self.ssh_key.public_key_openssh,
                opts=pulumi.ResourceOptions(parent=deployment),
            )

        instance = aws.ec2.Instance(
            f"{name}-instance",
            instance_type=config["instance_type"],
            key_name=self.aws_key_pair.key_name if self.aws_key_pair is not None else None,
            ami=image.id,
            subnet_id=subnet.id,
            vpc_security_group_ids = [firewall.id] if firewall is not None else None,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        if self.ssh_key is not None:
            self.run_command(instance)

        return instance


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
            image = self.image.get_instance(deployment, deployment, "gcp", region)

        metadata = None
        if self.ssh_key is not None:
            metadata = {
                "ssh-keys": self.ssh_key.public_key_openssh.apply(
                    lambda pub: f"{self.ssh_user}:{pub}"
                )
            }

        instance = gcp.compute.Instance(
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
            metadata=metadata,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        if self.ssh_key is not None:
            self.run_command(instance)
    
        return instance
    

    def run_command(self, instance):
        connection = {
            "host": instance.public_ip,
            "user": self.ssh_user,
            "private_key": self.ssh_key.private_key_pem,
            "port": 22,
        }
        
        copy_init = command.remote.CopyToRemote(
            f"{self.name}-copy-init",
            connection=connection,
            source=FileAsset("./init.sh"),
            remote_path=f"/home/{self.ssh_user}/init.sh",
            opts=pulumi.ResourceOptions(parent=instance, depends_on=[instance]),
        )

        run_init = command.remote.Command(
            f"{self.name}-run-init",
            connection=connection,
            create=f"chmod +x /home/{self.ssh_user}/init.sh && sudo /home/{self.ssh_user}/init.sh",
            opts=pulumi.ResourceOptions(parent=instance, depends_on=[copy_init, instance]),
        )