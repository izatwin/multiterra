from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Set

import pulumi
import pulumi_aws as aws


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


class DeploymentState:
    def __init__(self):
        self._component_states: Dict[GeneralizedCR, _ComponentDeploymentState] = {}
        self._providers: Dict[str, pulumi.ProviderResource] = {}

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

    def get_provider(self, provider: str, region: str, parent: pulumi.Resource) -> pulumi.ProviderResource:
        cache_key = _target_key(provider, region)
        if cache_key in self._providers:
            return self._providers[cache_key]

        if provider == "aws":
            aws_provider = aws.Provider(
                cache_key,
                region=region,
                opts=pulumi.ResourceOptions(parent=parent),
            )
            self._providers[cache_key] = aws_provider
            return aws_provider

        raise ValueError(f"Provider {provider} not implemented")


class Deployment(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        roots: List["GeneralizedCR"],
        providers: Set[str],
        regions: Set[str],
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__("custom:resources:Deployment", name, opts=opts)
        self._roots = [root for root in roots if root is not None]
        self._deployment_state = DeploymentState()

        for root in self._roots:
            root.deploy(self._deployment_state, providers, regions)


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

    def get_instance(self, deployment: DeploymentState, provider: str, region: str):
        return deployment.get_instance(self, provider, region)

    def deploy(self, deployment: DeploymentState, providers: Set[str], regions: Set[str]):
        for dep in self._deps:
            dep.deploy(deployment, providers, regions)

        for provider in providers:
            create_func = getattr(self, f"_create_{provider}", None)
            if create_func is None or not callable(create_func):
                raise ValueError(f"Provider {provider} not implemented on {type(self)}")
            for region in regions:
                if deployment.has_instance(self, provider, region):
                    continue
                deployment.set_instance(self, provider, region, create_func(deployment, region))

    def resource_name_prefix(self, provider: str, region: str) -> str:
        return f"{provider}-{region}-{type(self).__name__}-{self.name}"
