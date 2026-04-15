from typing import Optional, TypedDict

import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp

from multiterra.generalized_cr import Deployment, GeneralizedCR


class GeneralizedBucketArgs(TypedDict):
    public_access: bool


class GeneralizedBucket(GeneralizedCR):
    def __init__(
        self,
        name: str,
        args: GeneralizedBucketArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        # Buckets generally have no dependencies, so deps is an empty list []
        super().__init__("multiterra:storage:GeneralizedBucket", name, [], opts=opts)
        self.public_access = args["public_access"]

    def _create_aws(self, deployment: Deployment, region: str) -> aws.s3.BucketV2:
        provider = deployment.get_deployment_provider("aws", region)

        # Create the S3 Bucket
        bucket = aws.s3.BucketV2(
            self.resource_name_prefix("aws", region),
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )

        # Handle Public Access Block based on your generic args
        aws.s3.BucketPublicAccessBlock(
            f"{self.name}-pab",
            bucket=bucket.id,
            block_public_acls=not self.public_access,
            block_public_policy=not self.public_access,
            opts=pulumi.ResourceOptions(parent=bucket, provider=provider),
        )
        return bucket

    def _create_gcp(self, deployment: Deployment, region: str) -> gcp.storage.Bucket:
        # Note: You will need to implement get_deployment_provider for "gcp"
        # in generalized_cr.py first!
        provider = deployment.get_deployment_provider("gcp", region)

        return gcp.storage.Bucket(
            self.resource_name_prefix("gcp", region),
            location=region.upper(),
            opts=pulumi.ResourceOptions(parent=deployment, provider=provider),
        )
