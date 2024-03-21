import boto3

class IAMManager:
    def __init__(self):
        self.iam_client = boto3.client('iam')

    def get_user(self, username):
        try:
            response = self.iam_client.get_user(UserName=username)
            return response['User']
        except self.iam_client.exceptions.NoSuchEntityException:
            print(f"User '{username}' not found.")
            return None
    
    def delete_user(self, username):
        self.iam_client.delete_user(UserName=username)
        print(f"User '{username}' deleted successfully.")

    def list_access_keys(self, username):
        response = self.iam_client.list_access_keys(UserName=username)
        return response['AccessKeyMetadata']

    def list_attached_policies(self, username):
        response = self.iam_client.list_attached_user_policies(UserName=username)
        return response['AttachedPolicies']

    def delete_access_key(self, username, access_key_id):
        self.iam_client.delete_access_key(UserName=username, AccessKeyId=access_key_id)

    def detach_policy(self, username, policy_arn):
        self.iam_client.detach_user_policy(UserName=username, PolicyArn=policy_arn)

    def delete_policy(self, policy_arn):
        self.iam_client.delete_policy(PolicyArn=policy_arn)

    def manage_user(self, username):
        user = self.get_user(username)

        if user:
            access_keys = self.list_access_keys(username)
            attached_policies = self.list_attached_policies(username)

            if access_keys:
                delete_keys = input("User has access keys. Do you want to delete them? (yes/no): ").lower() == 'yes'
                if delete_keys:
                    for key in access_keys:
                        self.delete_access_key(username, key['AccessKeyId'])
                    print("Access keys deleted successfully.")

            if attached_policies:
                
                print("User has attached policies:")
                for policy in attached_policies:
                    print(policy['PolicyName'])

                delete_policies = input("Do you want to delete or detach them? (delete/detach/no): ").lower()
                if delete_policies == 'delete':
                    for policy in attached_policies:
                        self.detach_policy(username, policy['PolicyArn'])
                        self.delete_policy(policy['PolicyArn'])
                    print("Policies deleted successfully.")
                elif delete_policies == 'detach':
                    for policy in attached_policies:
                        self.detach_policy(username, policy['PolicyArn'])
                    print("Policies detached successfully.")
            
            self.delete_user(username)
            print("User Deletion completed.")
        else:
            print("Exiting...")

def main():
    iam_manager = IAMManager()
    username = input("Enter the username of the AWS IAM user: ")
    iam_manager.manage_user(username)

if __name__ == "__main__":
    main()
