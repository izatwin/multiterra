from multiterra import (
    Deployment,
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

    deployment = Deployment("aws_deployment", [low_instance, low_instance_two], {"aws"}, {"us-east-1"})


if __name__ == "__main__":
    main()
