import os
from dotenv import load_dotenv
from TwitchClouds import Emojis, ThirdpartyEmojis


load_dotenv()
USER_CLIENT_ID = os.getenv('USER_CLIENT_ID')
USER_ACCESS_TOKEN = os.getenv('USER_ACCESS_TOKEN')
BROADCASTER = os.getenv('BROADCASTER')

TEST_AUTH_HEADERS = {
    'Authorization': f'Bearer {USER_ACCESS_TOKEN}',
    'Client-Id': f'{USER_CLIENT_ID}'
}


def test_twitch_emojis():
    twitch_emojis = Emojis.GlobalEmojis(auth=TEST_AUTH_HEADERS)
    assert len(twitch_emojis._emojis) > 0, "Emojis.GlobalEmojis gives 0 emojis"


def test_channel_emojis():
    channel_emojis = Emojis.ChannelEmojis(auth=TEST_AUTH_HEADERS, channel=BROADCASTER)
    assert len(channel_emojis._emojis) > 0, "Emojis.ChannelEmojis gives 0 emojis"


def test_global_bttv_emojis():
    global_bttv = ThirdpartyEmojis.GlobalBTTV()
    assert len(global_bttv._emojis) > 0, "ThirdpartyEmojis.GlobalBTTV gives 0 emojis"


def test_global_ffz_emojis():
    global_ffz = ThirdpartyEmojis.GlobalFFZ()
    assert len(global_ffz._emojis) > 0, "ThirdpartyEmojis.GlobalFFZ gives 0 emojis"


def test_channel_bttv_emojis():
    channel_bttv_emojis = ThirdpartyEmojis.BTTV(channel=BROADCASTER, auth=TEST_AUTH_HEADERS)
    assert len(channel_bttv_emojis._emojis) > 0, "ThirdpartyEmojis.BTTV gives 0 emojis"


def test_channel_ffz_emojis():
    channel_ffz_emojis = ThirdpartyEmojis.FFZ(channel=BROADCASTER, auth=TEST_AUTH_HEADERS)
    assert len(channel_ffz_emojis._emojis) > 0, "ThirdpartyEmojis.FFZ gives 0 emojis"
