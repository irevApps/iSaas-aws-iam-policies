import boto3
import os
# Get AWS profile from environment variables or use 'default' profile
aws_profile = os.getenv('aws_profile', 'default')
#print("aws_profile",aws_profile)

class PolicyHelper:
    def __init__(self, profile_name='default'):
        self.session = boto3.Session(profile_name=profile_name)
        self.iam_client = self.session.client('iam')

