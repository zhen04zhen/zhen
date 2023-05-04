from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('97D4MU79prCTbdhJQea9GB4yqym0PGaoOGELtTlbtR3K3b+lJ5shg0bWQhRkDhmGrUkfb/kn8BndRjsbdmGqOj4H8AC8IuojBqDvzwruQwfVhkXKYZyFOQ3+jOnZwEJMZQvsn9Hy ibqrjAeFcL3VbgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('06d9f2cd281d81597e0a440f6abd7dff')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()