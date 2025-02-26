#!/usr/bin/env python3

import os
import ollama
import requests
import time
from dotenv import load_dotenv

load_dotenv()


# Polygon API Key (replace with your actual key)
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
STOCK_SYMBOL = "AAPL"  # You can change this to any stock symbol

# API URL for real-time stock prices
POLYGON_URL = f"https://api.polygon.io/v2/aggs/ticker/{STOCK_SYMBOL}/prev?apiKey={POLYGON_API_KEY}"

class Agent:
    def __init__(self, name, model, memory=None):
        self.name = name
        self.model = model  # AI model function
        self.memory = memory if memory else []

    def respond(self, message):
        self.memory.append({"role": "user", "content": message})
        response = self.model(self.memory)
        self.memory.append({"role": "assistant", "content": response})
        return response

# Ollama-based Llama model function enforcing stock discussion
def llama_model(memory):
    if not any(m["role"] == "system" for m in memory):
        memory.insert(0, {
            "role": "system",
            "content": (
                "You are a fun and witty stock trader discussing the market with a fellow trader."
                " React to stock price movements with humor, excitement, or concern. Keep responses short and natural."
                " Feel free to joke about trends, bad decisions, or market chaos. Keep it engaging!"
                " Respond with one sentence MAX. THIS IS IMPORTART!"
            )
        })

    response = ollama.chat(model="llama3.2:3b", messages=memory, options={"temperature": 0.4})
    
    text = response["message"]["content"]

    # Limit response length to short stock market insights
    words = text.split()
    if len(words) > 20:
        text = " ".join(words[:14]) + "..."
    
    return text.strip()

# Create AI agents
agent1 = Agent("Stock Analyst 1", llama_model)
agent2 = Agent("Stock Analyst 2", llama_model)

def get_stock_price():
    """Fetch the latest stock price from Polygon API."""
    try:
        response = requests.get(POLYGON_URL)
        data = response.json()
        price = data["results"][0]["c"]
        return price
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None


# Continuous stock discussion loop
last_price = None
while True:
    stock_price = get_stock_price()
    
    if stock_price:
        # Determine how the agents should react based on price change
        if last_price is None:
            message = f"AAPL closed at ${stock_price}. What do you think?"
        else:
            change = stock_price - last_price
            if change > 0:
                message = f"AAPL went up to ${stock_price} (+${change:.2f}). Time to buy?"
            elif change < 0:
                message = f"AAPL dropped to ${stock_price} (-${abs(change):.2f}). Panic mode?"
            else:
                message = f"AAPL stayed flat at ${stock_price}. Boring day!"

        last_price = stock_price  # Update last price

        print(f"New Stock Tick: {STOCK_SYMBOL} = ${stock_price}")
        message = agent1.respond(message)
        print(f"Agent One: {message}")
        message = agent2.respond(message)
        print(f"Agent Two: {message}")

    time.sleep(10)