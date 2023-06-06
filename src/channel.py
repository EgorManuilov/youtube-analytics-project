import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: int, channel_title: str, channel_description: str, channel_url: str,
                 channel_subscribes: str, video_count: str, views_count: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.channel_description = channel_description
        self.channel_url = channel_url
        self.channel_subscribes = channel_subscribes
        self.video_count = video_count
        self.views_count = views_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute(),
                         indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_name):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""

        data_channel = (
            {"channel_id": self.channel_id,
             "channel_title": self.channel_title,
             "description": self.channel_description,
             "url": self.channel_url,
             "video_count": self.video_count,
             "subscribers": self.channel_subscribes,
             "views_count": self.views_count
             }
        )

        with open(file_name, "w", encoding='utf-8') as file:
            json.dump(data_channel, file, indent=4, ensure_ascii=False)