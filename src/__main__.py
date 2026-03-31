# __main__.py



# ---------------
#     Imports
# ---------------



import pulumi
import pulumi_aws as aws

from vm.generalizedVM import GeneralizedVM



# ------------
#     Main
# ------------



def main1():
    return


def main():
    vpc = aws.ec2.Vpc(
        "vpc",
        cidr_block="10.0.0.0/16",
    )

    subnet = aws.ec2.Subnet(
        "subnet",
        vpc_id=vpc.id,
        cidr_block="10.0.1.0/24",
    )

    low_instance = GeneralizedVM(
        "lowInstance",
        provider="aws",
        tier="low",
        subnet=subnet,
    )


    temp = """
    vpc = GenNet()
    subnet = GenSub()
    vm = GenVM()

    vm.addProv("gpc")

    vpc.add("aws")

    vpc.add(subnet)
    vpc.add(subnet1)

    subnet.add(vm)
    subnet1.add(vm1)
    subnet1.add(vm2)
    """






if __name__ == "__main__":
    main()