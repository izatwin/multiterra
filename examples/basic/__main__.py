from multiterra import (
    Deployment,
    GeneralizedImage,
    GeneralizedSubnet,
    GeneralizedVM,
    GeneralizedVPC,
)

def main():
    vpc = GeneralizedVPC(
        "vpc",
        {
            "cidr_block": "10.0.0.0/16",
        },
    )

    subnet = GeneralizedSubnet(
        "subnet",
        {
            "vpc": vpc,
            "cidr_block": "10.0.1.0/24",
        },
    )

    image = GeneralizedImage(
        "tbd",
        {
            "image_blob": "",
        },
    )

    low_instance = GeneralizedVM(
        "lowInstance",
        {
            "tier": "low",
            "subnet": subnet,
            "image": image,
        },
    )

    high_instance = GeneralizedVM(
        "highInstance",
        {
            "tier": "high",
            "subnet": subnet,
            "image": image,
        },
    )

    Deployment("aws_deployment", [low_instance, high_instance], "aws", {"us-east-1"})


if __name__ == "__main__":
    main()
