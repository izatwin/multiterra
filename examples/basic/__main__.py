import pulumi_tls as tls

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
    GUARD = 1

    if GUARD:
        ssh_key = tls.PrivateKey(
            "ssh-key",
            algorithm="RSA",
            rsa_bits=4096,
        )

        ssh_user = "ec2-user"
    else:
        ssh_key = None
        ssh_user = None
    
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
        ssh_key=ssh_key,
        ssh_user=ssh_user,
    )

    medium_instance = GeneralizedVM(
        "mediumInstance",
        {
            "tier": "medium",
            "subnet": subnet,
            "image": image,
        },
        ssh_key=ssh_key,
        ssh_user=ssh_user,
    )

    high_instance = GeneralizedVM(
        "highInstance",
        {
            "tier": "high",
            "subnet": subnet,
            "image": image,
        },
        ssh_key=ssh_key,
        ssh_user=ssh_user,
    )

    app_storage = GeneralizedBucket(
        "app-data",
        {
            "public_access": False,
        },
    )

    Deployment(
        "aws_deployment",
        [low_instance, medium_instance, app_storage],
        "aws",
        {"us-east-1":None},
    )
    
    # Deployment(
    #     "gcp_deployment",
    #     [low_instance, high_instance, app_storage],
    #     "gcp",
    #     {"us-central1":"us-central1-a"},
    #     project_name="pulumi-test123",
    # )


if __name__ == "__main__":
    main()
