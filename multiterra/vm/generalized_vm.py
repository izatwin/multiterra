import pulumi

from ..generalized_cr import GeneralizedCR

from .utilsAwsVM import config_aws, createVM_AWS



# ---------------------------
#     class GeneralizedVM
# ---------------------------



class GeneralizedVM(GeneralizedCR):
    def __init__(self, name: str, tier: str, subnet, image=None, opts=None):
        super().__init__('custom:resources:GeneralizedVM', name, [subnet, image], opts=opts)
        self.subnet = subnet
        self.tier = tier
        self.name = name
        self.image = image

    def _create_aws(self, deployment, region):
        image = None if self.image is None else self.image.get_instance(deployment, "aws", region)
        instance = createVM_AWS(
            self,
            self.name,
            config_aws[self.tier],
            self.subnet.get_instance(deployment, "aws", region),
            image,
        )
        self.register_outputs({"aws_instance_id": instance.id}) # try to keep common output format
        return instance




