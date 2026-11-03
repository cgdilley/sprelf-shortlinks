
import os
import boto3
from pathlib import Path
from ruamel.yaml import YAML
import argparse
import string
import random
import botocore.client
import sys

Y = YAML()
Y.default_flow_style = False
Y.indent(mapping=2, sequence=2, offset=2)

HOME = Path.home()
SETTINGS = HOME / ".sprelf" / "links" / "settings.yaml"


#


def main():
    args = sys.argv[1:]
    settings = {}
    if os.path.exists(SETTINGS):
        with open(SETTINGS, "r") as f:
            settings = Y.load(f)

    parser = argparse.ArgumentParser(description="Create a shortened link.")
    parser.add_argument("link", help="The link to shorten.")
    parser.add_argument("--custom", "-c", help="A custom string to set as the link", default=None)
    parser.add_argument("--profile", help="The AWS profile to use", default=None)
    parser.add_argument("--domain", help="The domain to use for the link", default=None)
    parser.add_argument("--table", help="The table to register the link with.", default=None)

    options = parser.parse_args(args)

    profile_name = options.profile or settings.get("aws_profile")
    table_name = options.table or settings.get("table_name")
    domain_name = options.domain or settings.get("domain")

    if not profile_name or not table_name or not domain_name:
        raise ValueError("Missing required settings: aws_profile, table_name, domain")

    db = boto3.Session(profile_name=profile_name).client('dynamodb')

    short = options.custom if options.custom \
        else ''.join(random.choices(string.ascii_letters + string.digits, k=4))

    try:
        db.put_item(
            TableName=table_name,
            Item={
                "Key": {
                    "S": short
                },
                "Link": {
                    "S": options.link
                }
            },
            Expected={
                "Key": {
                    "Exists": False
                }
            }
        )
        print(f"{domain_name}/{short}")
    except botocore.client.ClientError as e:
        print(f"Error: {e}")