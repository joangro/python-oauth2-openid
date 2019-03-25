from google.oauth2 import service_account
import google.oauth2.credentials
import googleapiclient.discovery
import google_auth_oauthlib.flow
import jwt
import os

def add_member(mail):
    '''
    Add user to the project as an Editor
    '''
    credentials = service_account.Credentials.from_service_account_file(
                    '/srv/oauth/service_account.json',
                    scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build('cloudresourcemanager',
                                              'v1',
                                              credentials=credentials)

    project_id = os.environ('PROJECT_ID')

    policy = service.projects().getIamPolicy(
                resource=project_id,
                body={},
             ).execute()

    role="roles/editor"

    member="user:{}".format(mail)

    roles = [b['role'] for b in policy['bindings']]

    if role in roles:
        # if role already exists just append the user to it
        binding = next(b for b in policy['bindings'] if b['role'] == role)
        binding['members'].append(member)

    else:
        # Otherwise create the role and add the user
        binding = {'role': role, 'members': [member]}
        policy['bindings'].append(binding)

    # push new policy to the project
    policy = service.projects().setIamPolicy(
                resource=project_id,
                body={
                    'policy': policy,
                }
             ).execute()

    return "User {} added to project policy binding".format(mail)


