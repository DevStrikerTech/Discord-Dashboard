import os
import requests
from dotenv import load_dotenv

load_dotenv()


class DiscordOauth:
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = 'http://127.0.0.1:5000/dashboard'
    scope = 'identify%20guilds'
    login_url = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'
    token_url = 'https://discord.com/api/oauth2/token'
    api_endpoint = 'https://discord.com/api/v6'

    # Get access token
    @staticmethod
    def get_access_token(code):
        access_token_url = DiscordOauth.token_url

        access_token = requests.post(
            access_token_url,
            data={
                'client_id': DiscordOauth.client_id,
                'client_secret': DiscordOauth.client_secret,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': DiscordOauth.redirect_uri,
                'scope': DiscordOauth.scope

            }
        ).json()

        return access_token.get('access_token')

    # Get user
    @staticmethod
    def get_user(access_token):
        user_object = requests.get(
            url=f'{DiscordOauth.api_endpoint}/users/@me',
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()

        return user_object

    # Get user current guild
    @staticmethod
    def get_user_current_guild(access_token):
        user_guild_object = requests.get(
            url=f'{DiscordOauth.api_endpoint}/users/@me/guilds',
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()

        return user_guild_object