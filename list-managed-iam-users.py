import boto3
RefTag="iSaas-iam-deployer-cli"


iam_client = boto3.client('iam')

def list_users_and_policies():
    try:
        # List IAM users
        response = iam_client.list_users()
        if 'Users' in response:
            print("IAM Users:")
            for user in response['Users']:
                user_name = user['UserName']
                user_tags = iam_client.list_user_tags(UserName=user_name)['Tags']
                for tag in user_tags:
                    if tag['Key'] == "createdBy" and tag['Value'] == RefTag:
                        print(f"- {user_name}")
                        # List policies attached to the user
                        attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
                        if attached_policies:
                            print("       Policies:")
                            for policy in attached_policies:
                                print(f"         - {policy['PolicyArn']}")
                        else:
                            print("  No policies attached")
                        print()
                        break
        else:
            print("No IAM users found.")
    except Exception as e:
        print("Error listing users and policies:", str(e))

def main():
    list_users_and_policies()

if __name__ == "__main__":
    main()
