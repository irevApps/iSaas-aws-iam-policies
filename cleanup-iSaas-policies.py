import boto3



policies_names = [
    # Resources Managers policies :
    # "iSaas-s3-units-iam-manager-policy",
    "iSaas-s3-spaces-iam-manager-policy",
    # "iSaas-s3-manager-user-policy",
    # Sub Resources Agents policies :
    # "iSaas-s3-unit-user-policy",
    # "iSaas-s3-space-user-policy",
]

def get_aws_account_id():
    try:
        sts = boto3.client('sts')
        response = sts.get_caller_identity()
        return response['Account']
    except Exception as e:
        print(f"Error getting AWS account ID: {e}")
        return None

def generate_policy_arn(policy_name):
    aws_account_id = get_aws_account_id()
    if aws_account_id:
        return f"arn:aws:iam::{aws_account_id}:policy/{policy_name}"
    else:
        return None

def delete_iam_policy(policy_name):
    try:
        iam = boto3.client('iam')
        policy_arn = generate_policy_arn(policy_name)
        if policy_arn:
            iam.delete_policy(PolicyArn=policy_arn)
            print(f"Deleted policy '{policy_arn}'")
        else:
            print(f"Failed to generate policy ARN for '{policy_name}'")
    except iam.exceptions.NoSuchEntityException:
        print(f"Policy '{policy_name}' not found")
    except Exception as e:
        print(f"Error deleting policy '{policy_name}': {e}")

for policy_name in policies_names:
    delete_iam_policy(policy_name)