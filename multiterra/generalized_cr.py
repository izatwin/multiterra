from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Set

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp



def _target_key(provider: str, region: str, zone: str) -> str:
    if zone is not None:
        return f"{provider}-{zone}"
    
    return f"{provider}-{region}"



class _ComponentDeploymentState:
    def __init__(self):
        self._instance_matrix: Dict[str, Any] = {}


    def get_instance(self, provider: str, region: str, zone: str):
        return self._instance_matrix[_target_key(provider, region, zone)]


    def has_instance(self, provider: str, region: str, zone: str) -> bool:
        return _target_key(provider, region, zone) in self._instance_matrix


    def set_instance(self, provider: str, region: str, zone: str, instance: Any):
        self._instance_matrix[_target_key(provider, region, zone)] = instance



class Deployment(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        roots: List["GeneralizedCR"],
        provider: str,
        regions: Dict[str, Set[str]],
        project_name: Optional[str] =None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__("multiterra:common:Deployment", name, opts=opts)
        self._component_states: Dict[GeneralizedCR, _ComponentDeploymentState] = {}
        self._component_extras: Dict[GeneralizedCR, _ComponentDeploymentState] = {}
        self._region_providers: Dict[str, pulumi.ProviderResource] = {}
        self._roots = [root for root in roots if root is not None]
        self._project_name = project_name

        for root in self._roots:
            root.deploy(self, provider, regions, project_name)


    def _get_component_state(
        self, component: "GeneralizedCR"
    ) -> _ComponentDeploymentState:
        if component not in self._component_states:
            self._component_states[component] = _ComponentDeploymentState()
        return self._component_states[component]


    def get_instance(self, component: "GeneralizedCR", provider: str, region: str, zone: str):
        return self._get_component_state(component).get_instance(provider, region, zone)


    def has_instance(
        self, component: "GeneralizedCR", provider: str, region: str, zone: str
    ) -> bool:
        return self._get_component_state(component).has_instance(provider, region, zone)


    def set_instance(
        self, component: "GeneralizedCR", provider: str, region: str, zone: str, instance: Any
    ):
        self._get_component_state(component).set_instance(provider, region, zone, instance)


    def get_extra(self, component: GeneralizedCR, key: str, provider: str, region: str, zone: str) -> Any:
        return self._component_extras[component][f"{key}-{_target_key(provider, region, zone)}"]


    def set_extra(self, component: GeneralizedCR, key: str, provider: str, region: str, zone: str, value: Any) -> None:
        if component not in self._component_extras:
            self._component_extras[component] = {}
        self._component_extras[component][f"{key}-{_target_key(provider, region, zone)}"] = value


    def get_deployment_provider(
        self, provider: str, region: str, zone: str
    ) -> pulumi.ProviderResource:
        cache_key = _target_key(provider, region, zone)
        if cache_key in self._region_providers:
            return self._region_providers[cache_key]

        if provider == "aws":
            aws_provider = aws.Provider(
                cache_key,
                region=region,
                opts=pulumi.ResourceOptions(parent=self),
            )
            self._region_providers[cache_key] = aws_provider
            return aws_provider

        if provider == "gcp":
            gcp_provider = gcp.Provider(
                cache_key,
                project=self._project_name,
                region=region,
                zone=zone,
                opts=pulumi.ResourceOptions(parent=self),
            )
            self._region_providers[cache_key] = gcp_provider
            return gcp_provider

        if provider == "gcp":
            gcp_provider = gcp.Provider(
                cache_key,
                region=region,
                opts=pulumi.ResourceOptions(parent=self),
            )
            self._region_providers[cache_key] = gcp_provider
            return gcp_provider

        raise ValueError(f"Unsupported provider: {provider}")



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


    def get_instance(self, deployment: Deployment, provider: str, region: str, zone: str):
        return deployment.get_instance(self, provider, region, zone)


    def deploy(self, deployment: Deployment, provider: str, regions: Dict[str, Set[str]], project_name: str):
        for dep in self._deps:
            dep.deploy(deployment, provider, regions, project_name)

        create_func = getattr(self, f"_create_{provider}", None)
        if create_func is None or not callable(create_func):
            raise ValueError(f"Provider {provider} not implemented on {type(self)}")
        
        if not regions:
            if provider == "aws":
                regions = {aws.config.region: set()}
            elif provider == "gcp":
                regions = {gcp.config.region: set()}

        for region in regions:
            if not regions[region]:
                if provider == "aws":
                    regions[region] = {None}
                elif provider == "gcp":
                    regions[region] = {gcp.compute.get_zones(project=project_name, region=region).names[0]}

            for zone in regions[region]:
                if not deployment.has_instance(self, provider, region, zone):
                    deployment.set_instance(
                        self, provider, region, zone, create_func(deployment, region, zone)
                    )


    def resource_name_prefix(self, provider: str, region: str, zone: str) -> str:
        if zone is not None:
            return f"{provider}-{zone}-{self.name}"
        
        return f"{provider}-{region}-{self.name}"


    def get_extra(self, deployment: Deployment, key: str, provider: str, region: str, zone: str) -> Any:
        return deployment.get_extra(self, key, provider, region, zone)


    def set_extra(self, deployment: Deployment, key: str, provider: str, region: str, zone: str, value: Any) -> None:
        deployment.set_extra(self, key, provider, region, zone, value)
