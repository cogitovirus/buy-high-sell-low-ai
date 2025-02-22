#!/usr/bin/env python3

import ollama

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

# Ollama-based Llama model function
def llama_model(memory):
    response = ollama.chat(model="llama3.2:3b", messages=memory)
    return response["message"]["content"]

# Create two agents using Ollama
agent1 = Agent("Alice", llama_model)
agent2 = Agent("Bob", llama_model)

# Start a conversation
message = "Hello, how are you?"
for _ in range(10):
    message = agent1.respond(message)
    print(f"Alice: {message}")
    message = agent2.respond(message)
    print(f"Bob: {message}")
