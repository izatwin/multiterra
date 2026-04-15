from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Set

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp


def _target_key(provider: str, region: str) -> str:
    return f"{provider}-{region}"


class _ComponentDeploymentState:
    def __init__(self):
        self._instance_matrix: Dict[str, Any] = {}

    def get_instance(self, provider: str, region: str):
        return self._instance_matrix[_target_key(provider, region)]

    def has_instance(self, provider: str, region: str) -> bool:
        return _target_key(provider, region) in self._instance_matrix

    def set_instance(self, provider: str, region: str, instance: Any):
        self._instance_matrix[_target_key(provider, region)] = instance


class Deployment(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        roots: List["GeneralizedCR"],
        provider: str,
        regions: Dict[str, str],
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__("multiterra:common:Deployment", name, opts=opts)
        self._component_states: Dict[GeneralizedCR, _ComponentDeploymentState] = {}
        self._providers: Dict[str, pulumi.ProviderResource] = {}
        self._roots = [root for root in roots if root is not None]

        for root in self._roots:
            root.deploy(self, provider, regions)

    def _get_component_state(self, component: "GeneralizedCR") -> _ComponentDeploymentState:
        if component not in self._component_states:
            self._component_states[component] = _ComponentDeploymentState()
        return self._component_states[component]

    def get_instance(self, component: "GeneralizedCR", provider: str, region: str):
        return self._get_component_state(component).get_instance(provider, region)

    def has_instance(self, component: "GeneralizedCR", provider: str, region: str) -> bool:
        return self._get_component_state(component).has_instance(provider, region)

    def set_instance(self, component: "GeneralizedCR", provider: str, region: str, instance: Any):
        self._get_component_state(component).set_instance(provider, region, instance)

    def get_deployment_provider(self, provider: str, region: str, zone:str) -> pulumi.ProviderResource:
        cache_key = _target_key(provider, region)
        if cache_key in self._providers:
            return self._providers[cache_key]

        if provider == "aws":
            aws_provider = aws.Provider(
                cache_key,
                region=region,
                opts=pulumi.ResourceOptions(parent=self),
            )
            self._providers[cache_key] = aws_provider
            return aws_provider
        
        if provider == "gcp":
            gcp_provider = gcp.Provider(
                cache_key,
                project=f"pulumi-test123",
                region=region,
                zone=zone,
                opts=pulumi.ResourceOptions(parent=self),
            )
            self._providers[cache_key] = gcp_provider
            return gcp_provider

        raise ValueError(f"Provider {provider} not implemented")



class GeneralizedCR(pulumi.ComponentResource):
    def __init__(
        self,
        identifier: str,
        name: str,
        deps: Sequence["GeneralizedCR"],
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(identifier, name, opts=opts)
        self.name = name
        self._deps = [dep for dep in deps if dep is not None]

    def get_instance(self, deployment: Deployment, provider: str, region: str):
        return deployment.get_instance(self, provider, region)

    def deploy(self, deployment: Deployment, provider: str, regions: Dict[str, str]):
        for dep in self._deps:
            dep.deploy(deployment, provider, regions)

        create_func = getattr(self, f"_create_{provider}", None)
        if create_func is None or not callable(create_func):
            raise ValueError(f"Provider {provider} not implemented on {type(self)}")
        for region, zone in regions.items():
            if not deployment.has_instance(self, provider, region):
                deployment.set_instance(self, provider, region, create_func(deployment, region, zone))

    def resource_name_prefix(self, provider: str, region: str) -> str:
        return f"{provider}-{region}-{type(self).__name__}-{self.name}"