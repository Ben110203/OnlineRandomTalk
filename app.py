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

BACKEND_SERVUCE = "http://35.229.156.92:7705"

app = Flask(__name__)

LINE_CHANNEL_SECRET = 'e9d5b7f1223e54b57a458d4c82eff1fc'
LINE_CHANNEL_ACCESS_TOKEN = 'h6rGRksS2ZRJl4xFvfv2tDrBiAwTVUEPMtczNSy8cwe6yLbJ87wleDMyhIIF6+lwsDCR1XMBf8MCqDjegzEzKxyiF1hBOrkgZAIxoBQKlq55fSRnVtQx2F7XNgzhpBbXqcZcWbwjFFpXj0Uia4F12wdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
