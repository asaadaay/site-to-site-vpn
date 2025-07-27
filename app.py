#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.stack import SiteToSiteVpnStack


app = cdk.App()
stack_name = app.node.try_get_context("stack")

SiteToSiteVpnStack(
    app, 
    stack_name,
    stack_name=stack_name,
)

app.synth()
