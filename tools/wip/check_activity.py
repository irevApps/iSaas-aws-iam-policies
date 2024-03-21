import boto3
from datetime import datetime, timedelta

iam_client = boto3.client('iam')

def get_confirmation(message):
    while True:
        response = input(f"{message} (yes/no): ").strip().lower()
        if response in ['yes', 'no']:
            return response == 'yes'
        print("Invalid input. Please enter 'yes' or 'no'.")

def get_policy_arn_by_name(policy_name):
    try:
        response = iam_client.list_policies(Scope='Local')
        for policy in response['Policies']:
            if policy['PolicyName'] == policy_name:
                return policy['Arn']
        print(f"IAM policy '{policy_name}' not found.")
    except Exception as e:
        print(f"Error retrieving policy ARN for {policy_name}: {str(e)}")
    return None

def collect_user_policies(user_name):
    attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
    return attached_policies

def collect_user_dependencies(user_name):
    dependencies = []
    access_keys = iam_client.list_access_keys(UserName=user_name)['AccessKeyMetadata']
    if access_keys:
        dependencies.extend({ "type" : "access_key" , "list" : access_keys , "msg" : [f"IAM access key '{key['AccessKeyId']}'" for key in access_keys ]})

    attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
    if attached_policies:
        dependencies.extend({ "type" : "policy" , "list" : attached_policies , "msg" : [f"IAM attached policy '{policy['PolicyArn']}'" for policy in attached_policies]})

    # attached_groups = iam_client.list_groups_for_user(UserName=user_name)['Groups']
    # if attached_groups:
    #     dependencies.extend({ "type" : "access_key" , "list" : access_keys , "msg" : [f"IAM group '{group['GroupName']}' (ID: {group['GroupId']})" for group in attached_groups]})

    return dependencies

def check_user_activity(cloudtrail_client, username):
    try:
        # Get the current time and the time 24 hours ago
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)

        # Lookup events associated with the IAM user
        response = cloudtrail_client.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'Username',
                    'AttributeValue': username
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=1,
            ReverseOrder=True
        )

        # Check if there are any events associated with the user
        if response['Events']:
            event = response['Events'][0]
            return "Recent activity of IAM user '{}':\nEvent name: {}\nEvent time: {}\nEvent source: {}".format(
                username, event['EventName'], event['EventTime'], event['EventSource'])
        else:
            return f"No recent activity found for IAM user '{username}'."
    except Exception as e:
        return f"Error checking user activity: {str(e)}"

def delete_user_and_policy():
    iam_client = boto3.client('iam')
    cloudtrail_client = boto3.client('cloudtrail', region_name='us-west-1')

    user_name = input("Enter the IAM user to delete (leave empty to skip): ").strip()
    if user_name:
        try:
            response = iam_client.get_user(UserName=user_name)
            dependencies = collect_user_dependencies(user_name)

            if get_confirmation("Do you want to delete the user ?"):
                iam_client.delete_user(UserName=user_name)
                print(f"IAM user '{user_name}' has been deleted.")
                
            if dependencies:
                print(f"IAM user '{user_name}' has the following dependencies:")
                for dependency in dependencies:
                    print(f"  - {dependency}")
                    if(dependency.type == "policy"):
                        policies = dependency.list
                    if(dependency.type == "access_keys"):
                        access_keys = dependency.list
                #user_activity = check_user_activity(cloudtrail_client, user_name)
                #print("Infos , user got been already used ",user_activity)
                if get_confirmation("Do you want to delete the user along with its dependencies?"):
                    iam_client.delete_policy(PolicyArn=policy_arn)
                    print(f"IAM policy '{policy_arn}' has been deleted.")


            if get_confirmation(f"Do you want to delete IAM user '{user_name}'?"):
                iam_client.delete_user(UserName=user_name)
                print(f"IAM user '{user_name}' has been deleted.")
        except iam_client.exceptions.NoSuchEntityException:
            print(f"IAM user '{user_name}' not found.")

    policy_name = input("Enter the IAM policy to delete (leave empty to skip): ").strip()
    if policy_name:
        policy_arn = get_policy_arn_by_name(policy_name)
        if policy_arn:
            try:
                response = iam_client.get_policy(PolicyArn=policy_arn)
                attached_users = iam_client.list_entities_for_policy(PolicyArn=policy_arn, EntityFilter='User')['PolicyUsers']
                attached_groups = iam_client.list_entities_for_policy(PolicyArn=policy_arn, EntityFilter='Group')['PolicyGroups']

                dependencies = []
                if attached_users:
                    dependencies.extend([f"IAM user '{user['UserName']}' (ID: {user['UserId']})" for user in attached_users])

                if attached_groups:
                    dependencies.extend([f"IAM group '{group['GroupName']}' (ID: {group['GroupId']})" for group in attached_groups])

                if dependencies:
                    print(f"IAM policy '{policy_arn}' is attached to the following dependencies:")
                    for dependency in dependencies:
                        print(f"  - {dependency}")
                    if not get_confirmation("Do you want to delete the policy along with its dependencies?"):
                        return

                if get_confirmation(f"Do you want to delete IAM policy '{policy_arn}'?"):
                    iam_client.delete_policy(PolicyArn=policy_arn)
                    print(f"IAM policy '{policy_arn}' has been deleted.")
            except iam_client.exceptions.NoSuchEntityException:
                print(f"IAM policy '{policy_arn}' not found.")

def main():
    delete_user_and_policy()

if __name__ == "__main__":
    main()
