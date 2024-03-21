
# Usage : 


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