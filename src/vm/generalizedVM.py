# generalizedVM.py



# ---------------
#     Imports
# ---------------



import pulumi

from vm.utilsAwsVM import config_aws, createVM_AWS



# ---------------------------
#     class GeneralizedVM
# ---------------------------



class GeneralizedVM(pulumi.ComponentResource):
    def __init__(self, name: str, provider: str, tier: str, subnet, ami=None, opts=None):
        super().__init__('custom:resources:GeneralizedVM', name, opts=opts)

        if provider == "aws":
            self.instance = createVM_AWS(self, name, config_aws[tier], subnet, ami)

            self.register_outputs({"instance_id": self.instance.id})
        else:
            raise ValueError("Provider not implemented")


    