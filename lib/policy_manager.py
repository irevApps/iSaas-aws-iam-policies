import boto3
import os

class PolicyManager:
    def __init__(self):
        self.iam_client = boto3.client('iam')

    def deploy_policy(self, policy_name, policy_document):
        try:
            self.iam_client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=policy_document
            )
            print(f"Policy {policy_name} deployed successfully.")
        except self.iam_client.exceptions.EntityAlreadyExistsException:
            print(f"Policy {policy_name} already exists. Skipping deployment.")
        except Exception as e:
            print(f"Error deploying policy {policy_name}: {str(e)}")

    def delete_policy(self, policy_arn):
        try:
            self.iam_client.delete_policy(PolicyArn=policy_arn)
            print(f"Policy {policy_arn} deleted successfully.")
        except Exception as e:
            print(f"Error deleting policy {policy_arn}: {str(e)}")
