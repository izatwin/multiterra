# GeneralizedVM.py



# ---------------
#     Imports
# ---------------



import pulumi

from vm.utilsAwsVM import config_aws, createVM_AWS



# ---------------------------
#     class GeneralizedVM
# ---------------------------



class GeneralizedVM(pulumi.ComponentResource):
    def __init__(self, name: str, tier: str, subnet, image=None, opts=None):
        super().__init__('custom:resources:GeneralizedVM', name, opts=opts)
        self.subnet = subnet
        self.instance = dict()
        self.tier = tier
        self.name = name
        self.image = image

    def set_providers(self, providers: List[str]):
        self.subnet.set_providers(providers) # Add providers to all dependencies first
        self.image.set_providers(providers)
        for p in providers:
            if p in self.instance:
                continue
            if p == "aws":
                self.instance["aws"] = createVM_AWS(self, self.name, config_aws[self.tier], self.subnet, self.image.instance["aws"])
                self.register_outputs({"aws_instance_id": self.instance["aws"].id}) # try to keep common output format
            else:
                raise ValueError("Provider not implemented")






