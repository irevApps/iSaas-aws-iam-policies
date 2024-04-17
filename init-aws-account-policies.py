import os
import boto3
from lib.env_loader import load_env
from lib.policy_manager import PolicyManager


# Define paths to IAM policies
policy_paths = [
    # Resources Managers policies :
    "data/policies/provider/iSaas-s3-units-iam-manager-policy.json",
    "data/policies/provider/iSaas-s3-spaces-iam-manager-policy.json",
    "data/policies/managers/iSaas-s3-manager-user-policy.json",
    # Sub Resources Agents policies :
    "data/policies/agents/iSaas-s3-unit-user-policy.json",
    "data/policies/agents/iSaas-s3-space-user-policy.json",
]

iam_manager = PolicyManager()

# Deploy each policy
for policy_path in policy_paths:
    policy_name = os.path.splitext(os.path.basename(policy_path))[0]
    with open(policy_path, 'r') as policy_file:
        policy_document = policy_file.read()
        iam_manager.deploy_policy(policy_name, policy_document)
