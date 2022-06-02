import datetime
import typing
import twitch

from .Emojis import GlobalEmojis, ChannelEmojis


class User:
    def __init__(
            self,
            nickname: typing.Union[str],
            display_nickname: typing.Union[str],
            twitch_id: typing.Union[int],
            color: typing.Union[str],
    ):
        """ Twitch user representation for TwitchClouds;

        :param str nickname: Twitch user nickname
        :param str display_nickname: Twitch user displayable nickname
        :param int twitch_id: Twitch user ID
        :param str color: Twitch user color in chat
        """
        self.nickname = nickname
        self.display_nickname = display_nickname
        self.twitch_id = twitch_id
        self.color = color

    def __repr__(self):
        return f"User({self.display_nickname}, {self.nickname}, {self.twitch_id}, {self.color})"

    def __str__(self):
        return f"{self.nickname}"

    def __int__(self):
        return f"{self.twitch_id}"


class Message:
    def __init__(
            self,
            text: typing.Union[str],
            timestamp: typing.Union[datetime.date],
    ):
        """ Twitch chat message representation for TwitchClouds"""
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        return f"Message({self.timestamp}, {self.text})"

    def __str__(self):
        return f"{self.text}"


class Client:
    def __init__(self, app_api: twitch.helix.Helix, user_api: typing.Tuple):
        """ Client for working with official Twitch API and parsing data from
        unofficial API"""

        self._client_id = app_api.api.client_id
        self._client_secret = app_api.api.client_secret
        self._helix = app_api
        # Auth Headers
        self.auth = {
            'Authorization': f'Bearer {user_api[1]}',
            'Client-Id': f'{user_api[0]}'
        }

    def get_vods(
            self,
            user: twitch.helix.User,
            date: typing.Union[datetime.date] = None,
            start: typing.Union[datetime.date] = datetime.date.min,
            end: typing.Union[datetime.date] = datetime.date.max
    ):
        vods = []

        if date is None and start == datetime.date.min and end == datetime.date.max:
            return list(user.videos())

        for video in user.videos():
            created_at_str = video.created_at.replace('T', '|').replace('Z', '')
            created_at = datetime.datetime.strptime(created_at_str, '%Y-%m-%d|%H:%M:%S').date()
            if date is not None and created_at == date:
                vods.append(video)
            elif date is None and start <= created_at <= end:
                vods.append(video)

        return vods

    def get_chat_logs(
            self,
            videos: typing.List[twitch.helix.Video],
    ) -> typing.List[typing.Tuple[User, Message]]:
        """ Retrieving chat history of any stream"""
        logs = []

        for number, video in enumerate(videos):
            start_number_of_messages = len(logs)

            for i, comment in enumerate(self._helix.video(video.id).comments):
                print(f'\r[{number+1}/{len(videos)}] Video("{video.title}", {video.url}): Collecting vod comment №{i}{"."*(i%3+1)}{" "*(3-i%3+1)}', end='')

                created_at_str = comment.created_at.replace('T', '|').replace('Z', '')
                try:
                    created_at = datetime.datetime.strptime(created_at_str, '%Y-%m-%d|%H:%M:%S.%f').date()
                except ValueError:
                    created_at = datetime.datetime.strptime(created_at_str, '%Y-%m-%d|%H:%M:%S').date()

                logs.append((
                    User(
                        nickname=comment.commenter.name,
                        display_nickname=comment.commenter.display_name,
                        twitch_id=int(comment.commenter.id),
                        color=comment.message.user_color
                    ),
                    Message(
                        text=comment.message.body,
                        timestamp=created_at
                    ),
                ))
            print(f"\nCollected:\n"
                  f" from this VOD - {len(logs) - start_number_of_messages} messages\n"
                  f" total - {len(logs)} messages")

        return logs