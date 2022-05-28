import typing
import requests

from ..Erorrs import TwitchAPI


class Emoji:
    def __init__(
            self,
            name: typing.Union[str],
            images: typing.Any,
            emoji_id: typing.Union[int],
            source: typing.Union[str],
    ):
        self.name = name
        self.images = images
        self.emoji_id = emoji_id
        self.source = source

    def __repr__(self):
        return f"Emoji(source='{self.source}', name='{self.name}', id='{self.emoji_id}', preview='{list(self.images.values())[-1]}')"

    def __str__(self):
        return f"Emoji(source='{self.source}', name='{self.name}', id='{self.emoji_id}', preview='{list(self.images.values())[-1]}')"


class BaseEmojiSource(object):

    def __init__(self, auth: typing.Union[typing.Dict[str, str], None] = None, channel: typing.Union[str, None] = None):
        self._channel = channel
        self._auth = auth
        self._emojis = self._get_all_emojis()

    def _get_all_emojis(self) -> typing.List[typing.Union[Emoji, None]]:
        return []

    def _get_broadcaster_id(self) -> typing.Union[int]:
        response = requests.get(
            'https://api.twitch.tv/helix/users',
            params={'login': f'{self._channel}'},
            headers=self._auth
        ).json()

        # Handling API errors. [ method: chat/emotes ]
        if 'error' in response and response['status'] == 401:
            raise TwitchAPI.AuthentificationError(response)
        elif 'error' in response and response['status'] != 200:
            raise TwitchAPI.HelixAPIError(response)

        data = response["data"]

        if not data:
            raise TwitchAPI.UserNotFoundError(response)

        return data[0]["id"]

    def as_names(self):
        return [emoji.name for emoji in self._emojis]

    def as_ids(self):
        return [emoji.emoji_id for emoji in self._emojis]


class GlobalEmojis(BaseEmojiSource):
    API_ENDPOINT = 'https://api.twitch.tv/helix/chat/emotes/global'
    SOURCE_NAME = 'global'

    def _get_all_emojis(self) -> typing.List[typing.Union[Emoji, None]]:
        response = requests.get(self.API_ENDPOINT, headers=self._auth).json()

        # Handling API errors. [ method: chat/emotes/global]
        if 'error' in response and response['status'] == 401:
            raise TwitchAPI.AuthentificationError(response)
        elif 'error' in response and response['status'] != 200:
            raise TwitchAPI.HelixAPIError(response)
        if 'data' not in response:
            return []

        emoji_list, emojis = response["data"], []
        for emoji in emoji_list:
            emojis.append(Emoji(emoji["name"], emoji["images"], emoji["id"], source=self.SOURCE_NAME))

        return emojis


class ChannelEmojis(BaseEmojiSource):
    API_ENDPOINT = 'https://api.twitch.tv/helix/chat/emotes'
    SOURCE_NAME = 'channel'

    def _get_all_emojis(self) -> typing.List[typing.Union[Emoji, None]]:
        response = requests.get(
            self.API_ENDPOINT,
            params={'broadcaster_id': self._get_broadcaster_id()},
            headers=self._auth
        ).json()

        # Handling API errors [ method: users ]
        if 'error' in response and response['status'] == 401:
            raise TwitchAPI.AuthentificationError(response)
        elif 'error' in response and response['status'] != 200:
            raise TwitchAPI.HelixAPIError(response)
        if 'data' not in response:
            return []

        emoji_list, emojis = response["data"], []
        for emoji in emoji_list:
            emojis.append(Emoji(emoji["name"], emoji["images"], emoji["id"], source=self.SOURCE_NAME))

        return emojis
