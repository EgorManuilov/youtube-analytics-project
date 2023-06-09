import json
import os
from googleapiclient.discovery import build
from functools import total_ordering


@total_ordering
class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = "https://www.youtube.com/channel/" + self.__channel_id
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.subscribers = self.channel['items'][0]['statistics']['subscriberCount']
        self.views_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.__class__.__name__}, ({self.url})"

    def __add__(self, other):
        if isinstance(other, Channel):
            return int(self.subscribers) + int(other.subscribers)
        return NotImplementedError

    def __sub__(self, other):
        if isinstance(other, Channel):
            return int(self.subscribers) - int(other.subscribers)
        return NotImplementedError

    def __lt__(self, other):
        if isinstance(other, Channel):
            return int(self.subscribers) < int(other.subscribers)
        return NotImplementedError

    def __eq__(self, other):
        if isinstance(other, Channel):
            return int(self.subscribers) == int(other.subscribers)
        return NotImplementedError

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute(),
                         indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_name):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""

        data_channel = (
            {"channel_id": self.__channel_id,
             "channel_title": self.title,
             "description": self.description,
             "url": self.url,
             "video_count": self.video_count,
             "subscribers": self.subscribers,
             "views_count": self.views_count
             }
        )

        with open(file_name, "w", encoding='utf-8') as file:
            json.dump(data_channel, file, indent=4, ensure_ascii=False)
