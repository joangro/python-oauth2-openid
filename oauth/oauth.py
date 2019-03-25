from flask import (
                     redirect, request, Blueprint, session, render_template, url_for
            )

from   google.oauth2 import service_account
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import hashlib, os
import requests
import jwt

bp = Blueprint('oauth', __name__)

@bp.route('/')
def init():
    '''
    Main application page
    '''
    return render_template('index.html')


@bp.route('/openid')
def openid():
    '''
    First step to authenticate using OpenID
    '''
    session['state'] = hashlib.sha256(os.urandom(1024)).hexdigest()

    client_id = os.environ['CLIENT_ID']
    redirect_uri = os.environ['REDIRECT_URI']

    authorization_url = "https://accounts.google.com/o/oauth2/v2/auth?" \
                        "client_id={}&" \
                        "response_type=code&" \
                        "scope=openid%20email&" \
                        "redirect_uri={}&" \
                        "state={}".format(client_id, redirect_uri, session['state'])

    return redirect(authorization_url)

@bp.route('/redirected')
def redirected():
    '''
    Second step when redirected from the aforementioned methods.
    This handler, along with its URI needs to be Authorized in the Client ID configuration.
    For example: https://my-project.appspot.com/redirected
    '''
    if request.args.get('state', '') != session['state']:
        return "error", 401

    # Fetch discovery document
    r = requests.get('https://accounts.google.com/.well-known/openid-configuration')

    # Fetch token_endpoint uri
    token_endpoint = r.json()['token_endpoint']

    # Exchange code for access token

    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    redirect_uri = os.environ['REDIRECT_URI']

    data ={'code': request.args.get('code'),
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

    r = requests.post(token_endpoint, data=data)

    print("Status: {}".format(str(r.status_code)))

    parsed_r = r.json()

    import pprint
    pprint.pprint(parsed_r)

    access_token = parsed_r['access_token']
    id_token = parsed_r['id_token']

    # decode token to get user email
    decoded_id = jwt.decode(id_token, verify=False, algorithms='HS256')

    # Check account domain
    if decoded_id['hd'] == 'my-domain-example.com':
        '''
        Decode id token from the response.
        This example uses the SA in 'service_account.json' to add an email to the project IAM 
        '''
        mail = decoded_id['email']
        from .iam import add_member
        _ = add_member(mail)

        return redirect(url_for(".accepted"))

    return redirect(url_for(".denied"))

@bp.route('/accepted')
def accepted():
    '''
    User has been accepted in the project with those credentials
    '''
    
    return render_template('accepted.html', link={'project': os.environ['PROJECT_LINK']})

@bp.route('/denied')
def denied():
    '''
    User has been denied access to the project
    '''
    return render_template('denied.html')


