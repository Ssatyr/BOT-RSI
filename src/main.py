from typing import Final 
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from calculator import fetch_spot_data, fetch_spot_rsi
import asyncio
from logger_config import setup_logging
setup_logging()
import logging

# Load the token from the .env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
if len(TOKEN) == 0:
    logging.error("The Discord token is missing in the .env file.")
    exit(1)

try:
    CHANNEL_ID: Final[int] = int(os.getenv('CHANNEL_ID'))
except ValueError:
    logging.error("The channel ID is missing in the .env file or it is not a valid integer.")
    exit(1)

intents: Intents = Intents.default()
intents.typing = False
client: Client = Client(intents=intents)

latest_rsi_state = None # None, overbought, oversold

async def check_rsi():
    '''Check the RSI value every 10 seconds and send an alert if the value is above 70 or below 30.'''
    global latest_rsi_state
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        logging.error(f"Could not find channel with ID {CHANNEL_ID}")
        return
    

    logging.info("Starting RSI check loop.")
    while not client.is_closed():
        try:
            latest_rsi = fetch_spot_rsi()
            
            if latest_rsi > 70:
                if latest_rsi_state != 'overbought':
                    await channel.send(f"RSI Alert: High value of {latest_rsi} indicating overbought conditions.")
                    logging.info(f"RSI Alert: High value of {latest_rsi} indicating overbought conditions.")
                    latest_rsi_state = 'overbought'
            elif latest_rsi < 30:
                if latest_rsi_state != 'oversold':
                    await channel.send(f"RSI Alert: Low value of {latest_rsi} indicating oversold conditions.")
                    logging.info(f"RSI Alert: Low value of {latest_rsi} indicating oversold conditions.")
                    latest_rsi_state = 'oversold'
            else:
                latest_rsi_state = None
                
        except Exception as e:
            logging.error(f"An error occurred while checking RSI: {e}")
        await asyncio.sleep(10) 

@client.event
async def on_ready():
    logging.info(f'{client.user} has connected to Discord!')
    client.loop.create_task(check_rsi())

client.run(TOKEN)