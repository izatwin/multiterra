from __future__ import annotations

from typing import Optional, TypedDict

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp

from multiterra.generalized_cr import Deployment, GeneralizedCR


def is_ipv4(cidr: str) -> bool:
    return ":" not in cidr


class FirewallRule(TypedDict):
    port: int
    protocol: str  # "tcp", "udp", "icmp"
    cidr: str  # e.g. "0.0.0.0/0" for open, or a specific range


class GeneralizedFirewallArgs(TypedDict):
    vpc: GeneralizedCR
    ingress: list[FirewallRule] | None
    egress: list[FirewallRule] | None


class GeneralizedFirewall(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedFirewallArgs,
        opts: pulumi.ResourceOptions | None = None,
    ) -> None:
        super().__init__(
            "multiterra:network:GeneralizedFirewall",
            name,
            [args["vpc"]],
            opts=opts,
        )
        self.vpc = args["vpc"]
        self.ingress = args["ingress"]
        self.egress = args["egress"]

    def _create_aws(
        self, deployment: Deployment, region: str, zone: str,
    ) -> aws.ec2.SecurityGroup:
        provider = deployment.get_deployment_provider("aws", region, self)
        vpc = self.vpc.get_instance(deployment, "aws", region)

        instance = aws.ec2.SecurityGroup(
            self.resource_name_prefix("aws", region),
            name=self.resource_name_prefix("aws", region),
            vpc_id=vpc.id,
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        for egress in self.egress or []:
            aws.vpc.SecurityGroupEgressRule(
                f"{self.resource_name_prefix('aws', region)}-egress-{egress['port']}-{egress['protocol']}",
                security_group_id=instance.id,
                cidr_ipv4=egress["cidr"] if is_ipv4(egress["cidr"]) else None,
                cidr_ipv6=egress["cidr"] if not is_ipv4(egress["cidr"]) else None,
                from_port=egress["port"] if egress["protocol"] != "-1" else None,
                to_port=egress["port"] if egress["protocol"] != "-1" else None,
                ip_protocol=egress["protocol"],
                opts=pulumi.ResourceOptions(parent=instance, provider=provider),
            )

        for ingress in self.ingress or []:
            aws.vpc.SecurityGroupIngressRule(
                f"{self.resource_name_prefix('aws', region)}-ingress-{ingress['port']}-{ingress['protocol']}",
                security_group_id=instance.id,
                cidr_ipv4=ingress["cidr"] if is_ipv4(ingress["cidr"]) else None,
                cidr_ipv6=ingress["cidr"] if not is_ipv4(ingress["cidr"]) else None,
                from_port=ingress["port"] if ingress["protocol"] != "-1" else None,
                to_port=ingress["port"] if ingress["protocol"] != "-1" else None,
                ip_protocol=ingress["protocol"],
                opts=pulumi.ResourceOptions(parent=instance, provider=provider),
            )

        return instance


    def _create_gcp(self, deployment, region: str, zone: str):
        provider = deployment.get_deployment_provider("gcp", region, self)
        network = self.vpc.get_instance(deployment, "gcp", region)

        for ingress in self.ingress or []:
            allows=[gcp.compute.FirewallAllowArgs(
                protocol=ingress["protocol"],
                ports=[str(ingress["port"])] if ingress["protocol"] != "-1" else None,
            )] if ingress["protocol"] != "-1" else [
                gcp.compute.FirewallAllowArgs(protocol="all")
            ]
            
            gcp.compute.Firewall(
                f"{self.resource_name_prefix('gcp', region)}-ingress-{ingress['port']}-{ingress['protocol']}".lower().replace("_", "-"),
                name=f"{self.resource_name_prefix("gcp", region)}-ingress-{ingress['port']}-{ingress['protocol']}".lower().replace("_", "-"),
                network=network.id,
                direction="INGRESS",
                allows=allows,
                source_ranges=[ingress["cidr"]],
                opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
            )

        for egress in self.egress or []:
            allows=[gcp.compute.FirewallAllowArgs(
                protocol=egress["protocol"],
                ports=[str(egress["port"])] if egress["protocol"] != "-1" else None,
            )] if egress["protocol"] != "-1" else [
                gcp.compute.FirewallAllowArgs(protocol="all")
            ]
            
            gcp.compute.Firewall(
                f"{self.resource_name_prefix('gcp', region)}-egress-{egress['port']}-{egress['protocol']}".lower().replace("_", "-"),
                name=f"{self.resource_name_prefix("gcp", region)}-egress-{egress['port']}-{egress['protocol']}".lower().replace("_", "-"),
                network=network.id,
                direction="EGRESS",
                allows=allows,
                destination_ranges=[egress["cidr"]],
                opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
            )