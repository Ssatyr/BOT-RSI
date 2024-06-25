# Discord Bot Deployment Guide

This README provides instructions on how to deploy and run the Discord bot either locally or using Docker.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or higher
- Docker (for running within a container)
- Git (optional, for cloning the repository)

## Local Setup

1. **Clone the Repository** (if applicable):
   ```bash
   git clone https://github.com/Ssatyr/BOT-RSI.git
   cd BOT-RSI
   ```
2. **Install Dependencies**:
    Create a virtual environment and install the dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3. **Set Up Environment Variables**:
    Create a .env file in the root directory and add your Discord token:
    ```plaintext
    DISCORD_TOKEN=your_discord_bot_token_here
    CHANNEL_ID=your_channel_id_here
    ```
4. **Run the Bot**:
    Execute the main script to start the bot:
    ```bash
    python main.py
    ```

## Docker Setup

1. **Clone the Repository** (if applicable):
   ```bash
   git clone https://github.com/Ssatyr/BOT-RSI.git
   cd BOT-RSI
   ```
2. **Set Up Environment Variables**:
    Create a .env file in the root directory and add your Discord token:
    ```plaintext
    DISCORD_TOKEN=your_discord_bot_token_here
    CHANNEL_ID=your_channel_id_here
    ```
3. **Run the Bot**:
    Docker Deploy Instrucitons:
    ```bash
    docker build . -t "bot-rsi"
    docker run -d --env-file .env -t "bot-rsi"
    ```