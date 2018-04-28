from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Qe3hrlUjiTB8UqW4F6zlClqgZBDib3jfFuLRhijCLHSo0OR3wix9hc2kqXS5/3oxRbTxoa5lvSl2t28sy87bbecb3Y62si9dWPHm/BCqP6iOklLpm8v9eCdraYOuKq2wPNgMBsCUvWmEUlVhWC6myQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('df6333aba0c8b2fe37bfb8ee17f8c12e')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
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

import os
if __name__ == "__main__":
    app.run()
