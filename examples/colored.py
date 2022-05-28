import datetime

import twitch
from PIL import Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator

from TwitchClouds.Clouds import WordClouds
from TwitchClouds.Twitch import TwitchBot, Emojis, ThirdpartyEmojis


# Initialize bot for parsing messages
helix = twitch.Helix('app-client-id','app-client-secret')
bot = TwitchBot.Client(app_api=helix, user_api=('user-client-id', 'user-client-secret'))

# Getting VOD's chat log of streamer from 14/04/2022
channel = helix.user('bratishkinoff')
vods = bot.get_vods(user=channel, start=datetime.date(2022,4,14))
chat_history = bot.get_chat_logs(videos=vods, log_status=True)

# Getting user nicknames and messages text from chat logs
exclude_users, exclude_words = ['moobot', 'oldboty'], []
users_activity, words_activity = [], []
for user, message in chat_history:
    if user.nickname not in exclude_users:
        users_activity.append(user.display_nickname)
    words_activity += list(set(message.text.split()).difference(set(exclude_words)))

# Create image for coloring clouds
coloring = np.array(Image.open("brff-base-2.png"))
image_colors = ImageColorGenerator(coloring)
font = "arial.ttf"

# Generate word clouds
wordcloud_users = WordCloud(font_path=font, width=4000, height=4000, max_words=8000, mask=coloring, max_font_size=100, random_state=42, min_word_length=2).generate(' '.join(users_activity))
wordcloud_words = WordCloud(font_path=font, width=4000, height=4000, max_words=8000, mask=coloring, max_font_size=100, random_state=42, min_word_length=2).generate(' '.join(words_activity))

# Recolor clouds with coloring image
wordcloud_users.recolor(color_func=image_colors)
wordcloud_words.recolor(color_func=image_colors)

# Save images to file
wordcloud_users.to_file('users.png')
wordcloud_words.to_file('words.png')