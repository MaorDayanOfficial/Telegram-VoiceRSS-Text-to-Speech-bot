import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up the Telegram API with your token
updater = Updater(token='YOUR_TOKEN_HERE', use_context=True)
dispatcher = updater.dispatcher

# Define a function that will be called when the /start command is received
def start(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me some text and I'll send you back an audio file.")

# Set up a handler for the /start command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Set up a function to send a request to the VoiceRSS Text-to-Speech API
def send_to_voicerss(text):
  # Set up the parameters for the API request
  params = {
    'key': 'YOUR_API_KEY',
    'hl': 'en-us',
    'src': text,
    'r': '0',
    'c': 'MP3',
    'f': '44khz_16bit_stereo',
    'ssml': 'false',
    'b64': 'false'
  }

  # Send the request to the API and save the response
  response = requests.get('https://api.voicerss.org/', params=params)

  # Return the audio file from the response
  return response.content

# Set up a handler for all other messages
def echo(update, context):
  # Send the message text to the VoiceRSS Text-to-Speech API
  # and save the generated audio file to a variable
  audio = send_to_voicerss(update.message.text)

  # Send the audio file back to the user
  context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

# Start the bot
updater.start_polling()

#MaorDayan
#To use this code, you need to replace YOUR_TOKEN_HERE with your actual Telegram API token and YOUR_API_KEY with your VoiceRSS API key. You can sign up for a VoiceRSS API key at https://www.voicerss.org/register.aspx.
