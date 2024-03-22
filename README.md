
# iSaas AWS IAM Management Tool : 


## Context : 

This Python script is designed to assist with deploying required policies and IAM users to simplify connecting your AWS account as a provider on iSaas : the Infrastructure as a Service Management platform.

When integrating AWS services with third-party platforms, it's often necessary to manage IAM users and their access policies to ensure secure and controlled access to your AWS resources. This tool streamlines the process by allowing you to easily manage IAM users, access keys, and attached policies, ultimately facilitating the integration of your AWS account with iSaas.

# Terminology : 
iSaas will help you Manage you cloud capacity to manage :
- **Resources** : Cloud Resources , like ec2 instances , S3 buckets , ALBs ...
- **Infrasctures** : Composed Set of Resources as single system to Serve and deploy Apps and instances
- **Sub Resources** : Sub Elements or Sub spaces for a Cloud Resource : like S3 sub folder that been associated with a deployed app instance or dedicated folder to store backups of an infra ...


# Security and Scopes Limitation : 
iSaas is built to facilitate the managment of your aws Accounts and also to deploy Resources and infrastructures in a solide and secure way.

For that, each Resource or sub Resource Created by iSaas will be associated a new iam user to manage it if needed , specialy if those users credentials are shared with new apps instances or external agents.

A clair case will be the backups managment by iSaas , each managed infra will be associated with a sub folder of a shared S3 bucket dedécated for backups , each infra send and load its backups using isolated iam user that have only access to that bucket folder.

To make iSaas able to control you aws account with minimal permissions scopes , and make previous scenarios possible , we will need only to deploy the needed policies to your aws accout and give to iSaas a user that have only permission to create new iam users but limited by those policies.

You can see full list on data/polices.




## Usage : 


Init the aws account with required policies that iSaas needs to assign to sub users that will manage sub resources ( instances users for s3 , Resources Spaces users : S3 iam users ...)
All policies are listed in the data/policies folder :

```
    $ python init-aws-account-policies.py 

        Policy iSaas-s3-units-iam-manager-policy already exists. Skipping deployment.
        Policy isaas-s3-spaces-iam-manager-policy already exists. Skipping deployment.
        Policy iSaas-s3-manager-user-policy already exists. Skipping deployment.
        Policy iSaas-s3-unit-user-policy already exists. Skipping deployment.
        Policy isaas-s3-space-user-policy already exists. Skipping deployment.

```

Deploy the new iam user that will represente a new iSaas Provider on this aws account : 

```
    $ python deploy-new-iam-user.py 
        Enter username (default: iSaas-connector-24-03-21-11-36-28): 
        Enter policy name (default: iSaas-connector-24-03-21-11-36-28): 
        Paste the policy JSON below (press Ctrl+D to finish):
        << PAST POLICY JSON then click Enter then ctrl+D >>

        Does the above information look correct? (yes/no): yes

        IAM user iSaas-connector-24-03-21-11-36-28 created successfully.
        IAM policy iSaas-connector-24-03-21-11-36-28 created successfully.
        Policy attached to user iSaas-connector-24-03-21-11-36-28 successfully.


        Access key created successfully :
        aws_access_key_id = xxxxxxxxxxxxxxxx
        aws_secret_access_key = xxxxxxxxxxxxxxxx

```

List Existing Users that have been deployed with this cli :

```
    $ python list-managed-iam-users.py 

        IAM Users:
        - iSaas-connector-24-03-21-11-30-05
            Policies:
                - arn:aws:iam::xxxxxxxxxxxxx:policy/iSaas-connector-24-03-21-11-30-05

```

Delete an Iam user with its policy if needed :

```
    $ python delete-iam-user.py 
        Enter the username of the AWS IAM user: iSaas-connector-24-03-21-11-36-28
        User has access keys. Do you want to delete them? (yes/no): yes
        Access keys deleted successfully.
        User has attached policies:
        iSaas-connector-24-03-21-11-36-28
        Do you want to delete or detach them? (delete/detach/no): delete
        Policies deleted successfully.
        User 'iSaas-connector-24-03-21-11-36-28' deleted successfully.
        User Deletion completed.

        
```