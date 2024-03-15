from flask import Flask
app = Flask(__name__)

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
def handle_message(event):
    text1 = event.message.text

    messages =  [
        {
            'role':'system',
            'content': "你是一個專業的歷史老師，請以簡短的方式對話"
        },
        { # 這裏存放的是使用者增進輸入的訊息
            'role':'user',
            'content': "你好，很高興認識你"
        },
        { # 這個則是聊天機器人的回應訊息
            'role':'assistant',
            'content': f"你好！我也很高興認識你。有什麼外語方面的問題我可以幫助你解答嗎？"
        },
        { # 這個則是這次使用者輸入的訊息
            'role':'user',
            'content': f"{text1}"
        }
    ]

    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo-0125",
        temperature = 0.5,
    )
    try:
        ret = response['choices'][0]['message']['content'].strip()
    except:
        ret = '發生錯誤！'
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ret))

if __name__ == '__main__':
    app.run()
