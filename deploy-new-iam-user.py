import datetime
import sys
import json
from lib.env_loader import load_env
from lib.iam_manager import IAMManager


# # Load environment variables from .env file if it exists
# load_env()

def generate_proposed_username():
    now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    return f"iSaas-connector-{now}"

def pretty_print_policy(policy_document):
    print("Policy JSON:")
    print(json.dumps(policy_document, indent=4))

def main():
    iam_manager = IAMManager()

    # Get proposed username
    proposed_username = generate_proposed_username()
    username = input(f"Enter username (default: {proposed_username}): ") or proposed_username

    # Get policy name
    policy_name = input(f"Enter policy name (default: {username}): ") or username

    # Get policy JSON
    print("Paste the policy JSON below (press Ctrl+D to finish):")
    policy_json = sys.stdin.read().strip()

    # Validate policy JSON
    try:
        policy_document = json.loads(policy_json)
        pretty_print_policy(policy_document)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {str(e)}")
        return

    # Confirm with the user
    confirm = input("Does the above information look correct? (yes/no): ").lower()
    if confirm != "yes":
        print("Aborted.")
        return

    # Create IAM user, policy, attach policy to user, and create access key
    iam_manager.create_user_and_attach_policy(username, policy_name, policy_document)
    

if __name__ == "__main__":
    main()
