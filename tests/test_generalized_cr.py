from __future__ import annotations

import unittest
from unittest.mock import patch

from multiterra.generalized_cr import DeploymentState, GeneralizedCR


class _FakeDependency(GeneralizedCR):
    def __init__(self, name: str):
        super().__init__("test:FakeDependency", name, [])
        self.created = []

    def _create_aws(self, deployment: DeploymentState, region: str):
        instance = {"kind": "dependency", "name": self.name, "region": region}
        self.created.append(instance)
        return instance


class _FakeParent(GeneralizedCR):
    def __init__(self, name: str, dep: GeneralizedCR):
        super().__init__("test:FakeParent", name, [dep])
        self.dep = dep
        self.created = []

    def _create_aws(self, deployment: DeploymentState, region: str):
        dep_instance = self.dep.get_instance(deployment, "aws", region)
        instance = {"kind": "parent", "name": self.name, "region": region, "dep": dep_instance}
        self.created.append(instance)
        return instance


class GeneralizedCRDeploymentTests(unittest.TestCase):
    def setUp(self):
        self.component_resource_init = patch(
            "multiterra.generalized_cr.pulumi.ComponentResource.__init__",
            return_value=None,
        )
        self.component_resource_init.start()

    def tearDown(self):
        self.component_resource_init.stop()

    def test_shared_dependency_is_deployed_once_per_deployment(self):
        shared_dep = _FakeDependency("shared")
        parent_one = _FakeParent("one", shared_dep)
        parent_two = _FakeParent("two", shared_dep)
        deployment = DeploymentState()

        parent_one.deploy(deployment, {"aws"}, {"us-east-1"})
        parent_two.deploy(deployment, {"aws"}, {"us-east-1"})

        self.assertEqual(len(shared_dep.created), 1)
        self.assertEqual(parent_one.created[0]["dep"], parent_two.created[0]["dep"])

    def test_deployments_keep_state_isolated(self):
        dep = _FakeDependency("shared")
        parent = _FakeParent("one", dep)

        deployment_one = DeploymentState()
        deployment_two = DeploymentState()

        parent.deploy(deployment_one, {"aws"}, {"us-east-1"})
        parent.deploy(deployment_two, {"aws"}, {"us-east-1"})

        self.assertEqual(len(dep.created), 2)
        self.assertIsNot(
            dep.get_instance(deployment_one, "aws", "us-east-1"),
            dep.get_instance(deployment_two, "aws", "us-east-1"),
        )


if __name__ == "__main__":
    unittest.main()
