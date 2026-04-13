from __future__ import annotations

from typing import Any, Dict, List, Set

import pulumi


class _ComponentDeploymentState:
    def __init__(self):
        self.__instance_matrix: Dict[str, Any] = {}

    def get_instance(self, provider: str, region: str):
        return self.__instance_matrix[f"{provider}-{region}"]

    def has_instance(self, provider: str, region: str) -> bool:
        return f"{provider}-{region}" in self.__instance_matrix

    def set_instance(self, provider: str, region: str, instance: Any):
        self.__instance_matrix[f"{provider}-{region}"] = instance


class DeploymentState:
    def __init__(self):
        self.__component_states: Dict[GeneralizedCR, _ComponentDeploymentState] = {}

    def __get_component_state(self, component: "GeneralizedCR") -> _ComponentDeploymentState:
        if component not in self.__component_states:
            self.__component_states[component] = _ComponentDeploymentState()
        return self.__component_states[component]

    def get_instance(self, component: "GeneralizedCR", provider: str, region: str):
        return self.__get_component_state(component).get_instance(provider, region)

    def has_instance(self, component: "GeneralizedCR", provider: str, region: str) -> bool:
        return self.__get_component_state(component).has_instance(provider, region)

    def set_instance(self, component: "GeneralizedCR", provider: str, region: str, instance: Any):
        self.__get_component_state(component).set_instance(provider, region, instance)

class Deployment(pulumi.ComponentResource):
    def __init__(self, name: str, roots: List["GeneralizedCR"], providers: Set[str], regions: Set[str], opts=None):
        super().__init__("custom:resources:Deployment", name, opts=opts)
        self.name = name
        self.__roots = [root for root in roots if root is not None]
        self.__deployment_state = DeploymentState()

        for root in self.__roots:
            root.deploy(self.__deployment_state, providers, regions)

class GeneralizedCR(pulumi.ComponentResource):
    def __init__(self, identifier: str, name: str, deps: List["GeneralizedCR"], opts=None):
        super().__init__(identifier, name, opts=opts)
        self.identifier = identifier
        self.name = name
        self.__deps = [dep for dep in deps if dep is not None]

    def get_instance(self, deployment: DeploymentState, provider: str, region: str):
        return deployment.get_instance(self, provider, region)

    def deploy(self, deployment: DeploymentState, providers: Set[str], regions: Set[str]):
        # Update deps first
        for dep in self.__deps:
            dep.deploy(deployment, providers, regions)
        for p in providers:
            func_name = f"_create_{p}"
            create_func = getattr(self, func_name, None)
            if create_func is None or not callable(create_func):
                print(func_name)
                raise ValueError(f"Provider {p} not implemented on {type(self)}")
            for r in regions:
                if deployment.has_instance(self, p, r):
                    continue
                deployment.set_instance(self, p, r, create_func(deployment, r))
