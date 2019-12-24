class MyTubeChannel:
    def __init__(self, channel_name, channel_owner):
        self.name = channel_name
        self.owner = channel_owner
        self.subscribers = []
        self.videos = []
        self.playlists = {}

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
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


matt = MyTubeUser('Matt')
john = MyTubeUser('John')
erica = MyTubeUser('Erica')

tinfoil_hat = MyTubeChannel('Tinfoil Hat', john)
tinfoil_hat.subscribe(matt)
tinfoil_hat.subscribe(erica)
freshest_theories = ['Moon landing was fake', '9/11 was an inside job', 'Global warming is a hoax']
stay_woke_playlist = {'Stay Woke': freshest_theories}

for video in freshest_theories:
    tinfoil_hat.publish_video(video)

tinfoil_hat.publish_playlist(stay_woke_playlist)
