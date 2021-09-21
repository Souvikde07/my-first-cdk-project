from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import(
    aws_s3 as _s3,
    aws_iam as _iam,
    core
)


class MyFirstCdkProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #creating an S3 bucket
        _s3.Bucket(
            self,
            "myBucketId",    
            bucket_name = "myfirstcdkproject001",
            versioned = False,
            encryption = _s3.BucketEncryption.S3_MANAGED,
    	    block_public_access = _s3.BlockPublicAccess.BLOCK_ALL
        )
        #Creating another S3 bucket, and hence the bucket id has to be differnt than the previous bucket id
        object_mybucket = _s3.Bucket(
            self,
            "myBucketId1"
        )

        snstopicname ="abcxyz123"

        if not core.Token.is_unresolved(snstopicname) and len(snstopicname) > 10:
            raise ValueError("Maximum value can be only 10 characters")

        print(object_mybucket.bucket_name)

        _iam.Group(self, # creating an iam group
            "gid")

        Output_object1= core.CfnOutput(
            self,
            "myBucketOutput1",
            value = object_mybucket.bucket_name,
            description=f"My First CDK Bucket",
            export_name = "myBucketOutput1" 
        )

