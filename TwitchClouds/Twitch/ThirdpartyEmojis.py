import typing
import requests

from .Emojis import Emoji, BaseEmojiSource
from ..Erorrs import BttvAPI, FfzAPI


class GlobalBTTV(BaseEmojiSource):
    API_ENDPOINT = 'https://api.betterttv.net/3/cached/emotes/global'
    SOURCE_NAME = 'global_bttv'

    def _get_all_emojis(self) -> typing.List[Emoji]:
        response = requests.get(self.API_ENDPOINT).json()

        # Handling API errors. [ method: chat/emotes/global]
        if 'error' in response and response['status'] == 401:
            raise BttvAPI.BaseBttvAPIError(response)
        if not response:
            return []

        emoji_list, emojis = response, []
        for emoji in emoji_list:
            images = [f"https://cdn.betterttv.net/emote/{emoji['id']}/{size}x" for size in ['1', '2', '3']]
            emojis.append(Emoji(emoji["code"], images, emoji["id"], source=self.SOURCE_NAME))

        return emojis


class BTTV(BaseEmojiSource):
    API_ENDPOINT = 'https://api.betterttv.net/3/cached/users/twitch/'
    SOURCE_NAME = 'channel_bttv'

    def _get_all_emojis(self) -> typing.List[typing.Union[Emoji, None]]:
        response = requests.get(
            f"{self.API_ENDPOINT}{self._get_broadcaster_id()}"
        ).json()

        # Handling API errors. [ method: chat/emotes/global]
        if 'error' in response:
            raise BttvAPI.BaseBttvAPIError(response)
        if 'channelEmotes' not in response:
            return []

        emoji_list, emojis = response["channelEmotes"], []
        for emoji in emoji_list:
            images = [f"https://cdn.betterttv.net/emote/{emoji['id']}/{size}x" for size in ['1', '2', '3']]
            emojis.append(Emoji(emoji["code"], images, emoji["id"], source=self.SOURCE_NAME))

        return emojis


class GlobalFFZ(BaseEmojiSource):
    API_ENDPOINT = 'https://api.frankerfacez.com/v1/set/global'
    SOURCE_NAME = 'global_ffz'

    def _get_all_emojis(self) -> typing.List[Emoji]:
        response = requests.get(self.API_ENDPOINT).json()

        # Handling API errors. [ method: chat/emotes/global]
        if 'error' in response:
            raise FfzAPI.BaseFfzAPIError(response)
        if 'sets' not in response:
            return []

        emoji_list, emojis = response['sets'][str(response['default_sets'][0])]['emoticons'], []
        for emoji in emoji_list:
            images = [f"https://cdn.frankerfacez.com/emote/{emoji['id']}/{size}" for size in ['1', '2', '4']]
            emojis.append(Emoji(emoji["name"], images, emoji["id"], source=self.SOURCE_NAME))

        return emojis


class FFZ(BaseEmojiSource):
    API_ENDPOINT = 'https://api.frankerfacez.com/v1/room/id/'
    SOURCE_NAME = 'channel_ffz'

    def _get_all_emojis(self) -> typing.List[typing.Union[Emoji, None]]:
        response = requests.get(
            f"{self.API_ENDPOINT}{self._get_broadcaster_id()}"
        ).json()

        # Handling API errors. [ method: chat/emotes/global]
        if 'error' in response:
            raise FfzAPI.BaseFfzAPIError(response)
        if 'sets' not in response:
            return []

        emoji_list, emojis = response["sets"][str(response["room"]["set"])]["emoticons"], []
        for emoji in emoji_list:
            images = [f"https://cdn.frankerfacez.com/emote/{emoji['id']}/{size}" for size in ['1', '2', '4']]
            emojis.append(Emoji(emoji["name"], images, emoji["id"], source=self.SOURCE_NAME))

        return emojis