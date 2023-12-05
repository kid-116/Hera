import secrets
from urllib.parse import urlencode

from flask import Blueprint, flash, render_template, request, redirect, url_for, current_app, session, abort
import requests

from .forms import RegisterForm


users_bp = Blueprint("users", __name__,
                     template_folder="templates", url_prefix="/users")

login = current_app.config['LOGIN']


@login.user_loader
def load_user(id):
    return session['user']


@users_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@users_bp.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if session.get('user'):
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('users.oauth2_callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)


@users_bp.route('/callback/<provider>')
def oauth2_callback(provider):
    if session.get('user'):
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    current_app.logger.debug(request)
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('users.oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'}, verify=False)
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    }, verify=False)
    current_app.logger.debug(response.json())
    if response.status_code != 200:
        abort(401)
    username = provider_data['userinfo']['username'](response.json())

    # find or create the user in the database
    user = session.get('user')
    if user is None:
        user = {
            'username': username,
            'access_token': oauth2_token,
            'scopes': provider_data['scopes']
        }
        current_app.logger.debug(oauth2_token)
        session['user'] = user

    return redirect(url_for('index'))
