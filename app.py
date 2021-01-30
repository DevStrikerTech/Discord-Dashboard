from flask import Flask, request, redirect, render_template
from routes.discord_oauth import DiscordOauth

app = Flask(__name__)


# Route for index page
# Provides user login capabilities
@app.route('/login', methods=['GET'])
def login():
    return redirect(DiscordOauth.login_url)


# Route for dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    code = request.args.get('code')
    access_token = DiscordOauth.get_access_token(code)

    user_object = DiscordOauth.get_user(access_token)
    user_guild_object = DiscordOauth.get_user_current_guild(access_token)

    id, avatar, username, usertag = user_object.get('id'), user_object.get('avatar'), user_object.get('username'), \
                                    user_object.get('discriminator')

    return render_template('dashboard.html', render_user_avatar=f'https://cdn.discordapp.com/avatars/{id}/{avatar}.png',
                           render_username=f'{username}#{usertag}', render_guild=user_guild_object)


if __name__ == '__main__':
    app.run(debug=True)
