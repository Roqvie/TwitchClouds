import datetime
import twitch
from PIL import Image

from TwitchClouds.Clouds import WordClouds
from TwitchClouds.Twitch import TwitchBot, Emojis, ThirdpartyEmojis
from env import *


# Initialize bot for parsing messages
helix = twitch.Helix(client_id=APP_CLIENT_ID, client_secret=APP_CLIENT_SECRET)
bot = TwitchBot.Client(app_api=helix, user_api=(USER_CLIENT_ID, USER_ACCESS_TOKEN))
channel = helix.user(BROADCASTER)

vods = bot.get_vods(user=channel, start=datetime.date(2022, 5, 1), end=datetime.date(2022, 5, 31))
assert len(vods) > 0, '\n\nError! No VODs were found. Try another date or date interval.'
chat_history = bot.get_chat_logs(videos=vods)

# Getting all emojis for excluding in word cloud
twitch_emojis = Emojis.GlobalEmojis(auth=bot.auth).as_names()
channel_emojis = Emojis.ChannelEmojis(auth=bot.auth, channel=BROADCASTER).as_names()
global_bttv = ThirdpartyEmojis.GlobalBTTV().as_names()
channel_bttv = ThirdpartyEmojis.BTTV(auth=bot.auth, channel=BROADCASTER).as_names()
global_ffz = ThirdpartyEmojis.GlobalFFZ().as_names()
channel_ffz = ThirdpartyEmojis.FFZ(auth=bot.auth, channel=BROADCASTER).as_names()

# Getting user nicknames and messages text for word clouds
exclude_users = ['moobot', ]
exclude_words = twitch_emojis + channel_emojis + global_bttv + global_ffz + channel_bttv + channel_ffz

users_activity: list = []
words_activity: list = []
for i, log in enumerate(chat_history):
    print(f'\rCollecting words and users form chat history{"."*(i%3+1)}{" "*(3-i%3+1)}', end='')
    user, message = log
    if user.nickname not in exclude_users:
        users_activity.append(user.display_nickname)
    words_activity += list(set(message.text.split()).difference(set(exclude_words)))
print(f"\nCollected:\n"
      f" users - {len(users_activity)}\n"
      f" words - {len(words_activity)}\n")

assert len(users_activity) > 0, '\n\nError! No users were found. Try another VOD(s).'
assert len(words_activity) > 0, '\n\nError! No messages were found. Try another VOD(s).'

print("Generating word clouds...")
wordcloud_users = WordClouds.ColoredCloud(' '.join(users_activity), image=Image.open(BASE_FILE),
                                          font='examples/arial.ttf', max_font_size=100)
wordcloud_words = WordClouds.ColoredCloud(' '.join(words_activity), image=Image.open(BASE_FILE),
                                          font='examples/arial.ttf', max_font_size=100)

print("Saving word clouds as files...")
wordcloud_users.as_png(f'{OUTPUT_FILENAME}-users')
wordcloud_words.as_png(f'{OUTPUT_FILENAME}-words')
