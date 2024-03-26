import sys
import boto3
import json

def get_policy_document(policy_arn):
    # Create IAM client
    iam = boto3.client('iam')

    try:
        # Get the policy document
        response = iam.get_policy(PolicyArn=policy_arn)
        policy = response.get('Policy', {})
        if 'DefaultVersionId' in policy:
            version_id = policy['DefaultVersionId']
            version_response = iam.get_policy_version(PolicyArn=policy_arn, VersionId=version_id)
            policy_document = version_response['PolicyVersion']['Document']
            if isinstance(policy_document, str):
                return json.loads(policy_document)
            else:
                return policy_document
        else:
            print("Policy document not found for ARN:", policy_arn)
            return None
    except Exception as e:
        print("Error fetching policy document:", e)
        return None

def list_user_permissions(username):
    # Create IAM client
    iam = boto3.client('iam')

    # Get attached user policies
    attached_policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']

    # Get user policies
    user_policies = []
    for policy_info in attached_policies:
        policy_arn = policy_info['PolicyArn']
        policy_doc = get_policy_document(policy_arn)
        if policy_doc:
            user_policies.append(policy_doc)

    # Get groups for user
    groups = iam.list_groups_for_user(UserName=username)['Groups']
    group_policies = []
    for group in groups:
        for policy_info in iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']:
            policy_arn = policy_info['PolicyArn']
            policy_doc = get_policy_document(policy_arn)
            if policy_doc:
                group_policies.append(policy_doc)

    # Aggregate policies
    all_policies = user_policies + group_policies

    # Extract permissions
    permissions = set()
    for policy in all_policies:
        for statement in policy.get('Statement', []):
            if 'Action' in statement:
                if isinstance(statement['Action'], str):
                    permissions.add(statement['Action'])
                elif isinstance(statement['Action'], list):
                    permissions.update(statement['Action'])

    return list(permissions)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    permissions = list_user_permissions(username)
    print("Permissions for user '{}':".format(username))
    for permission in permissions:
        print(permission)
