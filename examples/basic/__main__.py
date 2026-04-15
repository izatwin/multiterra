from multiterra import (
    Deployment,
    GeneralizedBucket,
    GeneralizedImage,
    GeneralizedSubnet,
    GeneralizedVM,
    GeneralizedVPC,
    GeneralizedFirewall
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

    firewall = GeneralizedFirewall(
    "firewall",
    {
        "vpc": vpc,
        "ingress": [
            {"port": 22,  "protocol": "tcp", "cidr": "0.0.0.0/0"},
            {"port": 443, "protocol": "tcp", "cidr": "0.0.0.0/0"},
        ],
        "egress": [
            {"port": 0, "protocol": "-1", "cidr": "0.0.0.0/0"},
        ],
    },
)

    low_instance = GeneralizedVM(
        "lowInstance",
        {
            "tier": "low",
            "subnet": subnet,
            "image": image,
            "firewall": firewall,
        },
    )

    low_instance_two = GeneralizedVM(
        "lowInstanceTwo",
        {
            "tier": "low",
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
        [low_instance, low_instance_two, app_storage],
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
