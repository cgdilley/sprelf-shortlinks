
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
    if not os.path.exists(SETTINGS):
        raise FileNotFoundError(f"Settings file not found at {SETTINGS}")
    with open(SETTINGS, "r") as f:
        settings = Y.load(f)

    profile_name = settings.get("aws_profile")
    table_name = settings.get("table_name")

    if not profile_name or not table_name:
        raise ValueError("Missing required settings: aws_profile and table_name")

    db = boto3.Session(profile_name=profile_name).client('dynamodb')

    parser = argparse.ArgumentParser(description="Create a shortened link.")
    parser.add_argument("link", help="The link to shorten.")
    parser.add_argument("--custom", help="A custom string to set as the link", default=None)

    options = parser.parse_args(args)

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
        print(f"l.sprelf.com/{short}")
    except botocore.client.ClientError as e:
        print(f"Error: {e}")