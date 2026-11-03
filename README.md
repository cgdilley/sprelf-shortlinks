# Sprelf ShortLinks

A simple URL shortening service.

Create the backend stack using the provided CloudFormation template.

Install locally:

```
pip install -e <this directory>
```

To configure settings, create a `settings.yaml` file in the directory `~/.sprelf/links/`:

```yaml
aws_profile: <AWS CLI profile to use>
table_name: <Name of the DynamoDB table>
domain: <Domain name>
```

Create short links using the CLI:

```
sprelf-link <link> (--custom <custom path>)
```