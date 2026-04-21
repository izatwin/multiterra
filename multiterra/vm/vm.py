from __future__ import annotations

from typing import List, NotRequired, Optional, TypedDict, cast

import pulumi
import pulumi_aws as aws
import pulumi_command as command
import pulumi_gcp as gcp
import pulumi_tls as tls
from pulumi import FileAsset

from multiterra.network import GeneralizedFirewall, GeneralizedSubnet
from multiterra.vm.image import GeneralizedImage

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
    subnet: GeneralizedSubnet
    image: GeneralizedImage
    firewall: NotRequired[GeneralizedFirewall]
    associate_public_ip: NotRequired[bool]
    ssh_key: NotRequired[tls.PrivateKey]
    ssh_user: NotRequired[str]


class GeneralizedVM(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedVMArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        deps: List[GeneralizedCR] = [args["subnet"]]
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
        self.user_data = image.user_data
        self.firewall = firewall
        self.ssh_key = args.get("ssh_key", None)
        self.ssh_user = args.get("ssh_user", None)
        self.aws_key_pair = None
        self.associate_public_ip = args.get("associate_public_ip", False)

    def _create_aws(self, deployment: Deployment, region: str, zone: str):
        name = self.resource_name_prefix("aws", region, zone).lower().replace("_", "-")
        config = config_aws[self.tier]
        provider = deployment.get_deployment_provider("aws", region, zone)
        subnet = self.subnet.get_instance(deployment, "aws", region, zone)
        firewall = (
            None
            if self.firewall is None
            else self.firewall.get_instance(deployment, "aws", region, zone)
        )

        image = self.image.get_instance(deployment, "aws", region, zone)

        if (self.ssh_key is not None) and (self.aws_key_pair is None):
            self.aws_key_pair = aws.ec2.KeyPair(
                f"{name}-keypair",
                public_key=self.ssh_key.public_key_openssh,
                opts=pulumi.ResourceOptions(parent=deployment),
            )

        instance = aws.ec2.Instance(
            name,
            instance_type=config["instance_type"],
            key_name=self.aws_key_pair.key_name
            if self.aws_key_pair is not None
            else None,
            ami=image.id,
            subnet_id=subnet.id,
            vpc_security_group_ids=[firewall.id] if firewall is not None else None,
            user_data=self.user_data if self.user_data is not None else None,
            associate_public_ip_address=self.associate_public_ip,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        if self.associate_public_ip:
            pulumi.export(f"{name}-ip", instance.public_ip)

        # if self.ssh_key is not None:
        # self.run_command(instance)

        return instance

    def _create_gcp(self, deployment: Deployment, region: str, zone: str):
        name = self.resource_name_prefix("gcp", region, zone).lower().replace("_", "-")
        config = config_gcp[self.tier]
        provider = deployment.get_deployment_provider("gcp", region, zone)
        subnet = self.subnet.get_instance(deployment, "gcp", region, zone)
        image = self.image.get_instance(deployment, "gcp", region, zone)

        metadata = dict()
        if self.ssh_key is not None:
            metadata["ssh-keys"] = self.ssh_key.public_key_openssh.apply(
                lambda pub: f"{self.ssh_user}:{pub}"
            )

        if self.user_data is not None:
            metadata["user-data"] = self.user_data

        instance = gcp.compute.Instance(
            name,
            machine_type=config["machine_type"],
            zone=zone,
            boot_disk={
                "initialize_params": {
                    "image": image.self_link,
                }
            },
            network_interfaces=[
                {
                    "subnetwork": subnet.id,
                    "access_configs": [{}],
                }
            ],
            metadata=metadata,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        # if self.ssh_key is not None:
        # self.run_command(instance)

        if self.associate_public_ip:
            instance_ip = instance.network_interfaces.apply(
                lambda interfaces: (
                    interfaces[0].access_configs and interfaces[0].access_configs[0].nat_ip
                ),
            )

        pulumi.export(f"{name}-name", instance.name)

        if self.associate_public_ip:
            pulumi.export(f"{name}-ip", instance_ip)


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
            opts=pulumi.ResourceOptions(
                parent=instance, depends_on=[copy_init, instance]
            ),
        )
