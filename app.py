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
line_bot_api = LineBotApi('83o/LxwiZDexTSzhYZscZOB1VmSJdsLMICcgY5kbH7dOAxJeXpAu9yl9IWiqTU4kjb97ym6hv0drieXdtHR4EpnvgPlW7MaXOiO09LduXX/MtO/JoC4jj/YK6CmOQmmAWTFPWwl8Wq0SYZn5GOGjJwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('81aaf9b0388a99aeb843925e9977cea1')

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
