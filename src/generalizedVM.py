# ---------------
#     Imports
# ---------------



import pulumi

from utilsAwsVM import obtainConfig_AWS, createVM_AWS



# ---------------------------
#     class GeneralizedVM
# ---------------------------



class GeneralizedVM(pulumi.ComponentResource):
    def __init__(self, name: str, provider: str, tier: str):
        if provider == "aws":
            config = obtainConfig_AWS(self, tier)

            super().__init__('custom:resources:GeneralizedVM', name, {}, config["opts"])
            self.instance = createVM_AWS(self, name, config)

            self.register_outputs({"instance_id": self.instance.id})
        else:
            raise ValueError("Provider not implemented")


    