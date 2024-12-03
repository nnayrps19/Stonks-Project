import queue
 
class Publisher:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.subscribers = []
 
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
 
    def publish(self, message):
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)
 
class Subscriber:
    def __init__(self, name):
        self.name = name
 
    def receive(self, message):
        print(f"{self.name}"+"received message:"
              +f"{message}")
 
publisher = Publisher()
 
subscriber_1 = Subscriber("Subscriber 1")
subscriber_2 = Subscriber("Subscriber 2")
 
publisher.subscribe(subscriber_1)
publisher.subscribe(subscriber_2)
 
publisher.publish("Hello World")