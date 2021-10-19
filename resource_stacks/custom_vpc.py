from aws_cdk import core as cdk

from aws_cdk import (aws_ec2 as _ec2,aws_s3 as _s3,core)

class CustomVpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_configs = self.node.try_get_context('envs')['prod']

        custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            cidr = prod_configs['vpc_configs']['vpc_cidr'],
            max_azs= 2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name = "publicSubnet",cidr_mask = prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type = _ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name = "privateSubnet",cidr_mask = prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type = _ec2.SubnetType.PRIVATE
                ),
                _ec2.SubnetConfiguration(
                    name = "dbSubnet",cidr_mask = prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type = _ec2.SubnetType.ISOLATED
                )           
            ]
        )

        core.Tag.add(custom_vpc,"Owner","Coder-Souvik")
    	
        core.CfnOutput(self,
                        "CustomVpcOutput",
                        value=custom_vpc.vpc_id,
                        export_name="customVpcId")

        my_bkt = _s3.Bucket(self,"custombktId")

        core.Tag.add(my_bkt,"Owner","Coder_Boy_Souvik")


        #resource in same account.
        bkt_1=_s3.Bucket.from_bucket_name(
            self,
            "MyImportedBucket",
            "myfirstcdkproject001"
        )

        bkt_2 = _s3.Bucket.from_bucket_arn(
            self,
            "crossAccountBucket",
            "arn:aws:s3:::SAMPLE-CROSS-BUCKET"
        )
        #output for bkt_1
        core.CfnOutput(self,
                        "myimportedbucket",
                        value=bkt_1.bucket_name
                        )
        
        #importing a VPC
        vpc2 = _ec2.Vpc.from_lookup(self,
                                    "importedVPC",
                                   # is_default=True,
                                   vpc_id="vpc-885898e3"
                                   )
        #vpc2 output
        core.CfnOutput(self,
                        "importedVpc2",
                        value=vpc2.vpc_id
                        )
        
        #After importing next we are peering the old vpc with the newly imported VPC.
        peer_vpc= _ec2.CfnVPCPeeringConnection(self,
                                                "peerVpc12",
                                                peer_vpc_id=custom_vpc.vpc_id,
                                                vpc_id=vpc2.vpc_id)   