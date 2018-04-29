import logging
import time

from flask import Flask,request , abort
import requests
from linebot import (LineBotApi , WebhookHandler)

from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
MessageEvent,
TextMessage ,
TextSendMessage,
CarouselTemplate,
URITemplateAction,
TemplateSendMessage,
CarouselColumn
)

app = Flask(__name__)

LINE_CHANNEL_SECRET = '6a581aa9ecc578501d45db0af8d42b2d'
LINE_CHANNEL_ACCESS_TOKEN = 'LYwHL8AUdUHSTCjwP15S/6VGkKP7RUPE7Th8TRufAURcoPs9aNmonOZ90JctT0fYRbTxoa5lvSl2t28sy87bbecb3Y62si9dWPHm/BCqP6jAojyZZAs+eQ+HBofIGuFHlbcpq9l6lyvnXzo/l3BsagdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=['GET'])
def reply():
    return '200'

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            message)


if __name__ == "__main__":
    app.run()
