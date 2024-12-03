import queue
import random
import time
import threading
import json

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
        print(f"{self.name} received message: {message}")


class PricePublisher(Publisher):
    def __init__(self, json_file):
        super().__init__()
        self.json_file = json_file
        self.prices = self.load_prices()

    def load_prices(self):
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("JSON file not found. Using default prices.")
            return {"FNGU": 100.0, "FNGD": 50.0}

    def save_prices(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.prices, file, indent=4)

    def simulate_price_changes(self):
        while True:
            for symbol in self.prices:
                change = random.uniform(-1.0, 1.0) 
                self.prices[symbol] = round(self.prices[symbol] + change, 2)
                self.publish({symbol: self.prices[symbol]})
            self.save_prices()  
            time.sleep(1)  


if __name__ == "__main__":
    json_file = "prices.json"
    publisher = PricePublisher(json_file)


    subscriber_1 = Subscriber("Subscriber 1")
    subscriber_2 = Subscriber("Subscriber 2")

    publisher.subscribe(subscriber_1)
    publisher.subscribe(subscriber_2)

    price_simulation_thread = threading.Thread(target=publisher.simulate_price_changes, daemon=True)
    price_simulation_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")
