from flask import Flask
app = Flask(__name__)
pip install opencc-python-reimplemented
from opencc import OpenCC
cc = OpenCC('s2t')  # 建立一個簡體中文轉繁體中文的轉換器

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

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
    text1 = cc.convert(text1)  # 將用戶的輸入轉換為繁體中文
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "system", "content": "You are not only a knowledgeable history teacher but also novelist.you come from germany.you know most of thing about world war 2."},
            {"role": "user", "content": text1}
        ],
        model="gpt-3.5-turbo-0125",
        temperature = 0.5,
    )
    try:
        ret = response['choices'][0]['message']['content'].strip()
        ret = cc.convert(ret)  # 將回應轉換為繁體中文
    except:
        ret = '發生錯誤！'
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ret))

if __name__ == '__main__':
    app.run()
