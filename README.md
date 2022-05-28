# TwitchClouds

Instrument for creating word clouds of Twitch:
- Active chatters
- Most used words in messages

### Features

- Working with Helix API with twitch python library
- BTTV, FFZ, Twitch emoji support for exculding from wordclouds
- Working with images with PIL


### Installing　(Python 3.10 on Ubuntu)
```bash
python -m venv venv
venv/bin/activate
python -m pip install - r requirements.txt
```

### Example　

```python
import twitch
from PIL import Image

from TwitchClouds.Clouds import WordClouds
from TwitchClouds.Twitch import TwitchBot, Emojis, ThirdpartyEmojis


# Initialize bot for parsing messages
helix = twitch.Helix('<api-secret>')
bot = TwitchBot.Client(app_api=helix, user_api=('<client-id>', '<client-secret>'))

channel = helix.user('<tiwth-streaner-nickname>')
vods = bot.get_vods(user=channel)
chat_history = bot.get_chat_logs(videos=vods, log_status=True)

# Getting all emojis for excluding in word cloud
twitch_emojis = Emojis.GlobalEmojis(auth=bot.auth).as_names()
channel_emojis = Emojis.ChannelEmojis(auth=bot.auth, channel='<tiwth-streaner-nickname>').as_names()
global_bttv = ThirdpartyEmojis.GlobalBTTV().as_names()
channel_bttv = ThirdpartyEmojis.BTTV(auth=bot.auth, channel='<tiwth-streaner-nickname>').as_names()
global_ffz = ThirdpartyEmojis.GlobalFFZ().as_names()
channel_ffz = ThirdpartyEmojis.FFZ(auth=bot.auth, channel='<tiwth-streaner-nickname>').as_names()

# Getting user nicknames and messages text for word clouds
exclude_users = ['moobot']
exclude_words = twitch_emojis + channel_emojis + global_bttv + global_ffz + channel_bttv + channel_ffz

users_activity: list = []
words_activity: list = []
for user, message in chat_history:
    if user.nickname not in exclude_users:
        users_activity.append(user.display_nickname)
    words_activity += list(set(message.text.split()).difference(set(exclude_words)))

wordcloud_users = WordClouds.ColoredCloud(' '.join(users_activity), image=Image.open('examples/base.png'), font='examples/arial.ttf', max_font_size=50)
wordcloud_words = WordClouds.ColoredCloud(' '.join(words_activity), image=Image.open('examples/base.png'), font='examples/arial.ttf', max_font_size=50)

wordcloud_users.as_png('generated/', 'users')
wordcloud_words.as_png('generated/', 'words')
```

### Example image
![JesusAVGN](https://raw.githubusercontent.com/Roqvie/TwitchClouds/master/generated/hesus-users1.png)
