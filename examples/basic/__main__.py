import pulumi
import pulumi_cloudinit as cloudinit
import pulumi_tls as tls

from multiterra import (
    Deployment,
    GeneralizedBucket,
    GeneralizedFirewall,
    GeneralizedImage,
    GeneralizedSubnet,
    GeneralizedVM,
    GeneralizedVPC,
    ImageEnum,
)


def main():

    # Define non-pulumi resources
    with open("./cloudinit.yaml", "r") as config:
        cloudinit_config = cloudinit.get_config_output(
            gzip=False,
            base64_encode=False,
            parts=[
                {
                    "content_type": "text/cloud-config",
                    "content": config.read(),
                }
            ],
        )

    ssh_key = tls.PrivateKey(
        "ssh_key",
        algorithm="RSA",
        rsa_bits=4096,
    )
    ssh_user = "ubuntu"

    # Define generalized resources
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
        "ubuntu_image",
        {
            "image_name": ImageEnum.UBUNTU, "user_data": cloudinit_config.rendered
        },
    )

    firewall = GeneralizedFirewall(
        "firewall",
        {
            "vpc": vpc,
            "ingress": [
                {"port": 22, "protocol": "tcp", "cidr": "0.0.0.0/0"},
                {"port": 80, "protocol": "tcp", "cidr": "0.0.0.0/0"},
                {"port": 443, "protocol": "tcp", "cidr": "0.0.0.0/0"},
            ],
            "egress": [
                {"port": 0, "protocol": "-1", "cidr": "0.0.0.0/0"},
            ],
        },
    )

    low_instance = GeneralizedVM(
        "low_instance",
        {
            "tier": "low",
            "subnet": subnet,
            "image": image,
            "firewall": firewall,
            "ssh_key": ssh_key,
            "ssh_user": ssh_user,
            "associate_public_ip": True,
        },
    )

    medium_instance = GeneralizedVM(
        "medium_instance",
        {
            "tier": "medium",
            "subnet": subnet,
            "image": image,
        },
    )

    high_instance = GeneralizedVM(
        "high_instance",
        {
            "tier": "high",
            "subnet": subnet,
            "image": image,
        },
    )

    app_storage = GeneralizedBucket(
        "bucket",
        {
            "public_access": False,
        },
    )

    # Deployment(
    #     "defaults",
    #     [low_instance],
    #     "gcp",
    #     {},
    #     project_name="pulumi-test123",
    # )

    # Deployment(
    #     "aws_deployment",
    #     [low_instance, medium_instance, app_storage],
    #     "gcp",
    #     {"us-east1": {}},
    #     project_name="pulumi-test123",
    # )

    Deployment(
        "gcp_deployment",
        [low_instance, high_instance, app_storage],
        "gcp",
        {"us-central1":{"us-central1-a", "us-central1-b"}, "us-east1": {"us-east1-c"}},
        project_name="pulumi-test123",
    )

    pulumi.export("private_key", pulumi.Output.secret(ssh_key.private_key_pem))


if __name__ == "__main__":
    pass
    main()
