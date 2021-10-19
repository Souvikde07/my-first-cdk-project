#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

from resource_stacks.custom_vpc import CustomVpcStack

app = core.App()

CustomVpcStack(app, "my-custom-vpc-stack",
                env = core.Environment(account="426945086755",region="ap-south-1"))

core.Tag.add(app, key = "stack-team-support-email",
            value= app.node.try_get_context('envs')['prod']['stack-team-support-email']),

core.Tag.add(app, key = "stack-level-tagging",
            value= "sample_tag_value")

app.synth()
