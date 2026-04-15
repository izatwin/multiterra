from multiterra import (
    Deployment,
    GeneralizedBucket,
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

    app_storage = GeneralizedBucket(
        "app-data",
        {
            "public_access": False,
        },
    )

    Deployment(
        "aws_deployment",
        [low_instance, high_instance, app_storage],
        "aws",
        {"us-east-1":None},
    )
    
    Deployment(
        "gcp_deployment",
        [low_instance, high_instance, app_storage],
        "gcp",
        {"us-central1":"us-central1-a"},
    )


if __name__ == "__main__":
    main()
