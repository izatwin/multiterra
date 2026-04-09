from multiterra import (
    GeneralizedImage,
    GeneralizedSubnet,
    GeneralizedVM,
    GeneralizedVPC,
)

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


    low_instance.set_providers({"aws"})
    high_instance.set_providers({"aws"})

    low_instance.set_regions({"region"})
    high_instance.set_regions({"region"})


if __name__ == "__main__":
    main()
