import os

from dotenv import load_dotenv


load_dotenv()

class Config:
    MYSQL_HOST = os.environ['MYSQL_HOST']
    MYSQL_USER = os.environ['MYSQL_USER']
    MYSQL_PASSWORD = os.environ['MYSQL_USER']
    MYSQL_DB = os.environ['MYSQL_DATABASE']
    MYSQL_CURSORCLASS = 'DictCursor'

    ENV = 'development'
    DEBUG = True

    FLASK_APP = 'app.py'

    SECRET_KEY = 'secret_key'

    WSO2_CLIENT_ID = os.environ['WSO2_CLIENT_ID']
    WSO2_CLIENT_SECRET = os.environ['WSO2_CLIENT_SECRET']
    WSO2_HOST = os.environ['WSO2_HOST']

    OAUTH2_PROVIDERS = {
        'wso2': {
            'client_id': WSO2_CLIENT_ID,
            'client_secret': WSO2_CLIENT_SECRET,
            'authorize_url': f'{WSO2_HOST}/oauth2/authorize',
            'token_url': f'{WSO2_HOST}/oauth2/token',
            'userinfo': {
                'url': f'{WSO2_HOST}/oauth2/userinfo',
                'username': lambda json: json['sub'],
            },
            'scopes': ['openid', 'email', 'profile', 'friends_view3'],
        }
    }
