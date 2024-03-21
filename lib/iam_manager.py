import boto3
import json
import os
from datetime import datetime

# Get AWS profile from environment variables or use 'default' profile
#aws_profile = os.getenv('AWS_PROFILE', 'default')
def getTags():
    tags = [
        {'Key': 'createdBy', 'Value': 'iSaas-iam-deployer-cli'}, 
        {'Key': 'createdAt', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S') }
    ]
    return tags


class IAMManager:
    def __init__(self):
        #self.session = boto3.Session(profile_name=aws_profile)
        self.iam_client = boto3.client('iam')
    #============================================================================== helpers :
    def get_policy_by_name(self, policy_name):
        try:
            response = self.iam_client.list_policies(Scope='Local')
            for policy in response['Policies']:
                if policy['PolicyName'] == policy_name:
                    return policy
            print(f"Policy {policy_name} not found.")
        except Exception as e:
            print(f"Error retrieving policy ARN for {policy_name}: {str(e)}")
        return None
    #============================================================================== main functions
    def create_user(self, username):
        try:
            self.iam_client.create_user(UserName=username, Tags=getTags() )
            print(f"IAM user {username} created successfully.")
        except self.iam_client.exceptions.EntityAlreadyExistsException:
            print(f"IAM user {username} already exists. Skipping creation.")
        except Exception as e:
            print(f"Error creating user {username}: {str(e)}")
        return username  # Return username even if it already exists

    def create_policy(self, policy_name, policy_document):
        try:
            # Convert policy document to JSON string
            policy_document_str = json.dumps(policy_document)

            response = self.iam_client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=policy_document_str,  # Pass the JSON string
                Tags=getTags()
            )
            print(f"IAM policy {policy_name} created successfully.")
            return response['Policy']['Arn']
        except self.iam_client.exceptions.EntityAlreadyExistsException:
            print(f"IAM policy {policy_name} already exists. Skipping creation.")
            policy = self.get_policy_by_name(policy_name)
            if policy:
                return policy['Arn']
        except Exception as e:
            print(f"Error creating policy {policy_name}: {str(e)}")
        return None

    def attach_policy_to_user(self, username, policy_arn):
        try:
            response = self.iam_client.attach_user_policy(
                UserName=username,
                PolicyArn=policy_arn
            )
            print(f"Policy attached to user {username} successfully.")
            return policy_arn
        except self.iam_client.exceptions.EntityAlreadyExistsException:
            print(f"Policy is already attached to user {username}. Skipping attachment.")
            return self.get_attached_policy_arn(username, policy_arn)
        except Exception as e:
            print(f"Error attaching policy to user {username}: {str(e)}")
        return None

    def create_access_key(self, username):
        try:
            response = self.iam_client.create_access_key(UserName=username)
            print("Access key created successfully :")
            access_key = response['AccessKey']
            aws_access_key_id = access_key['AccessKeyId']
            aws_secret_access_key = access_key['SecretAccessKey']
            print(f"aws_access_key_id = {aws_access_key_id}")
            print(f"aws_secret_access_key = {aws_secret_access_key}")
            return {
                'aws_access_key_id': aws_access_key_id,
                'aws_secret_access_key': aws_secret_access_key
            }
        except Exception as e:
            print(f"Error creating access key for user {username}: {str(e)}")
            return None

    def create_user_and_attach_policy(self, username, policy_name, policy_document):
        print("\n")
        self.create_user(username)
        #print("\n")
        policy_arn = self.create_policy(policy_name, policy_document)
        #print("\n")
        #print("policy_arn",policy_arn)
        if policy_arn:
            self.attach_policy_to_user(username, policy_arn)

            print("\n")
            access_key = self.create_access_key(username)
            return access_key
        return None

