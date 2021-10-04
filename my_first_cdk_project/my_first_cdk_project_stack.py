from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import(
    aws_s3 as _s3,
    aws_iam as _iam,
    aws_kms as _kms,
    core
)

class MyArtifactBucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str,is_prod = False,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        mykey = _kms.key.from_key_arn(  self,
                                        "mykeyid",
                                        self.node.try_get_context('prod')['kms_arn'])


        # The code that defines your stack goes here
        if is_prod:
            artifactBucket = _s3.Bucket(self,
                                        "myProdArtifactBucketId",
                                        versioned =True, 
                                        encryption =_s3.BucketEncryption.KMS,
                                        encryption_key = mykey,
                                        removal_policy=core.RemovalPolicy.RETAIN)
        
        else:
            artifactBucket = _s3.Bucket(self,"myDevArtifactBucketId")