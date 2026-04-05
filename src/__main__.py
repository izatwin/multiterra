# __main__.py



# ---------------
#     Imports
# ---------------



import pulumi
import pulumi_aws as aws

from vm.GeneralizedVM import GeneralizedVM
from vm.GeneralizedImage import GeneralizedImage
from subnet import GeneralizedSubnet
from vpc import GeneralizedVPC

# ------------
#     Main
# ------------

def main():
    vpc = GeneralizedVPC(
        "vpc",
        "10.0.0.0/16",
    )

    subnet = GeneralizedSubnet(
        "subnet",
        vpc,
        "10.0.1.0/24",
    )

    image = GeneralizedImage("tbd")

    low_instance = GeneralizedVM(
        "lowInstance",
        tier="low",
        subnet=subnet,
        image=image,
    )

    high_instance = GeneralizedVM(
        "highInstance",
        tier="high",
        subnet=subnet,
        image=image,
    )


    low_instance.set_providers(["aws"]) # declares this vm and all dependencies on AWS
    high_instance.set_providers(["aws"]) # declares this vm and all dependencies on AWS only. Reuses existing subnet and vpc.


if __name__ == "__main__":
    main()
