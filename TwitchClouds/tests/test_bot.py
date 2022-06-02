import os
import datetime
from dotenv import load_dotenv
import twitch

from TwitchClouds.Twitch import TwitchBot


load_dotenv()
APP_CLIENT_ID = os.getenv('APP_CLIENT_ID')
APP_CLIENT_SECRET = os.getenv('APP_CLIENT_SECRET')
USER_CLIENT_ID = os.getenv('USER_CLIENT_ID')
USER_ACCESS_TOKEN = os.getenv('USER_ACCESS_TOKEN')
BROADCASTER = os.getenv('BROADCASTER')

TEST_AUTH_HEADERS = {
    'Authorization': f'Bearer {USER_ACCESS_TOKEN}',
    'Client-Id': f'{USER_CLIENT_ID}'
}


def test_retrieving_vods():
    helix = twitch.Helix(client_id=APP_CLIENT_ID, client_secret=APP_CLIENT_SECRET)
    bot = TwitchBot.Client(app_api=helix, user_api=(USER_CLIENT_ID, USER_ACCESS_TOKEN))
    channel = helix.user(BROADCASTER)
    vods = bot.get_vods(user=channel)
    assert len(vods) > 0, "User has no saved VODs or user with given access token cant retrieve it"
