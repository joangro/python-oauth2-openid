# Python OAuth 2.0 with OpenID

Skeleton for a base Python OAuth 2.0 application, using OpenID Connect.

## Description

This is an exemplified implementation of the [OAuth2.0 OpenID Connect documentation](https://developers.google.com/identity/protocols/OpenIDConnect).

It is done with [Flask](http://flask.pocoo.org/docs/1.0/) and [Flask Bootstrap](https://pythonhosted.org/Flask-Bootstrap/).

This is intended to be deployed in [App Engine Standard for Python3](https://cloud.google.com/appengine/docs/standard/python3/), however it can run locally given that you have the variables from the `env_variables` secrion in the `app.yaml` file present in the runtime environment, i.e. running `export PROJECT_ID='my-project-id'`
