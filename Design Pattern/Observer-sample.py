from abc import ABC, abstractmethod

# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

# Subject
class YouTubeChannel:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, observer: Observer):
        self.subscribers.append(observer)

    def unsubscribe(self, observer: Observer):
        self.subscribers.remove(observer)

    def notify_all(self, message: str):
        for subscriber in self.subscribers:
            subscriber.update(message)

    def upload_video(self, video_title: str):
        print(f"\n🎥 New video uploaded: {video_title}")
        self.notify_all(f"New video: {video_title}")

# Concrete Observers
class SubscriberA(Observer):
    def update(self, message: str):
        print(f"Subscriber A received: {message}")

class SubscriberB(Observer):
    def update(self, message: str):
        print(f"Subscriber B received: {message}")

# Example usage
channel = YouTubeChannel()

a = SubscriberA()
b = SubscriberB()

channel.subscribe(a)
channel.subscribe(b)

channel.upload_video("Design Patterns in Python")
channel.unsubscribe(b)
channel.upload_video("Trying after unsubscribe")