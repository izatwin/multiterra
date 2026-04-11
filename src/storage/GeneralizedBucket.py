import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp
from GeneralizedCR import GeneralizedCR


class GeneralizedBucket(GeneralizedCR):
    def __init__(
        self,
        name: str,
        public_access: bool = False,
        versioning: bool = False,
        opts=None,
    ):
        super().__init__("custom:resources:GeneralizedBucket", name, [], opts=opts)
        self.name = name
        self.public_access = public_access
        self.versioning = versioning

    def _create_aws(self, region: str):
        bucket = aws.s3.Bucket(
            self.name,
            versioning=aws.s3.BucketVersioningArgs(enabled=self.versioning),
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Handle AWS Public Access logic
        ownership = aws.s3.BucketOwnershipControls(
            f"{self.name}-oc",
            bucket=bucket.id,
            rule={"object_ownership": "BucketOwnerPreferred"},
            opts=pulumi.ResourceOptions(parent=self),
        )

        pab = aws.s3.BucketPublicAccessBlock(
            f"{self.name}-pab",
            bucket=bucket.id,
            block_public_acls=not self.public_access,
            block_public_policy=not self.public_access,
            ignore_public_acls=not self.public_access,
            restrict_public_buckets=not self.public_access,
            opts=pulumi.ResourceOptions(parent=self),
        )

        if self.public_access:
            aws.s3.BucketAclV2(
                f"{self.name}-acl",
                bucket=bucket.id,
                acl="public-read",
                opts=pulumi.ResourceOptions(parent=self, depends_on=[ownership, pab]),
            )

        self.register_outputs({"bucket_id": bucket.id})
        return bucket

    def _create_gcp(self, region: str):
        bucket = gcp.storage.Bucket(
            self.name,
            location=region,
            versioning=gcp.storage.BucketVersioningArgs(enabled=self.versioning),
            opts=pulumi.ResourceOptions(parent=self),
        )

        if self.public_access:
            gcp.storage.BucketIAMMember(
                f"{self.name}-iam",
                bucket=bucket.name,
                role="roles/storage.objectViewer",
                member="allUsers",
                opts=pulumi.ResourceOptions(parent=self),
            )

        self.register_outputs({"bucket_url": bucket.self_link})
        return bucket
