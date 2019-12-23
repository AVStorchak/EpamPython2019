class MyTubeChannel:
    def __init__(self, channel_name, channel_owner):
        self.name = channel_name
        self.owner = channel_owner
        self.subscribers = list()
        self.videos = []
        self.playlists = {}

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber) -> None:
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    def notify_subscribers(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

    def publish_video(self, video):
        self.videos.append(video)
        message = f"there is new video on '{self.name}' channel: '{video}'"
        self.notify_subscribers(message)

    def publish_playlist(self, playlist):
        self.playlists.update(playlist)
        message = f"there is new playlist on '{self.name}' channel: '{list(playlist.keys())[0]}'"
        self.notify_subscribers(message)


class MyTubeUser:
    def __init__(self, name: str):
        self._name = name

    def update(self, message):
        print(f"Dear {self._name}, {message}")
