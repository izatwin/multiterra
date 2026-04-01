# __main__.py



# ---------------
#     Imports
# ---------------



import pulumi
import pulumi_aws as aws

from vm.GeneralizedVM import GeneralizedVM



# ------------
#     Main
# ------------



def main1():
    return


def main():
    vpc = GeneralizedVpc(
        "vpc",
        cidr_block="10.0.0.0/16",
    )

    subnet = GeneralizedSubnet(
        "subnet",
        vpc=vpc,
        cidr_block="10.0.1.0/24",
    )

    low_instance = GeneralizedVM(
        "lowInstance",
        tier="low",
        subnet=subnet,
    )

    high_instance = GeneralizedVM(
        "highInstance",
        tier="high",
        subnet=subnet,
    )


    low_instance.set_providers(["aws", "gcp"]) # declares this vm and all dependencies on AWS and GCP
    high_instance.set_providers(["aws"]) # declares this vm and all dependencies on AWS only. Reuses existing subnet and vpc.


if __name__ == "__main__":
    main()
