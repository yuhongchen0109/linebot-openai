from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os
message_counter = 0  # 初始化訊息計數器

openai.api_key = os.getenv('OPENAI_API_KEY')
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler1 = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text1=event.message.text
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "system", "content": "You are not only a knowledgeable history teacher but also novelist.you come from germany.you know most of thing about world war 2.Please convert the output results into Traditional Chinese."},
            {"role": "user", "content": text1}
        ],
        model="gpt-3.5-turbo-0125",
        temperature = 0.5,
    )
    try:
        ret = response['choices'][0]['message']['content'].strip()
        message_counter += 1  # 每次傳送訊息時，將計數器加一
        print(f"已經傳送了 {message_counter} 則訊息")  # 打印出已經傳送的訊息數量
    except:
        ret = '發生錯誤！'
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ret))

if __name__ == '__main__':
    app.run()
