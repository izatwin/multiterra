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

    def add_providers(providers: str[]):
        self.subnet.add_providers(providers) # Add providers to all dependencies first
        self.image.add_providers(providers)
        for p in providers:
            if p = "aws":
                if provider == "aws":
                    if "aws" not in self.instance:
                        self.instance["aws"] = createVM_AWS(self, self.name, config_aws[self.tier], self.subnet, self.image.get_instance(aws))
                        self.register_outputs({"aws_instance_id": self.instance.id}) # try to keep common output format
                else:
                    raise ValueError("Provider not implemented")






