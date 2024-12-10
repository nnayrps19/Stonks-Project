import random
import time
import threading
from typing import Callable, List

class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback: Callable[[str, float], None]):

        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[str, float], None]):

        self.subscribers.remove(callback)

    def notify(self, stock: str, price: float):
   
        for subscriber in self.subscribers:
            subscriber(stock, price)

class StockPriceSimulator:
    def __init__(self, publisher: Publisher, stocks: List[str]):
        self.publisher = publisher
        self.prices = {stock: random.uniform(50, 500) for stock in stocks}  # Initial random prices

    def simulate_price_changes(self):
        """Simulate random price changes and notify the publisher."""
        while True:
            stock = random.choice(list(self.prices.keys()))
            delta = random.uniform(-5, 5)  # Random price change
            self.prices[stock] += delta
            self.prices[stock] = max(0, self.prices[stock])  # Ensure price doesn't go negative
            print(f"[Simulator] {stock} new price: {self.prices[stock]:.2f}")
            self.publisher.notify(stock, self.prices[stock])
            time.sleep(random.uniform(1, 3))  # Random interval between updates

class Subscriber:
    def __init__(self, name: str):
        self.name = name

    def update(self, stock: str, price: float):
        """Receive updates from the publisher."""
        print(f"[Subscriber: {self.name}] {stock} price updated to {price:.2f}")

if __name__ == "__main__":
    # Initialize publisher
    publisher = Publisher()

    # Create and subscribe subscribers
    subscriber1 = Subscriber("Trader A")
    subscriber2 = Subscriber("Investor B")
    
    publisher.subscribe(subscriber1.update)
    publisher.subscribe(subscriber2.update)

    # Initialize stock price simulator
    stocks = ["FNGU", "FNGD"]
    simulator = StockPriceSimulator(publisher, stocks)

    # Start simulation in a separate thread
    simulator_thread = threading.Thread(target=simulator.simulate_price_changes, daemon=True)
    simulator_thread.start()


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation stopped.")