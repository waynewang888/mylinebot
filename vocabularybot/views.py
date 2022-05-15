from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

class vocab():

    def getVoc(self):
        import openpyxl
        import pandas as pd
        import random
        n = []
        while len(n) < 5:
            num = random.randrange(716)
            if num not in n:
                n.append(num)
        df = pd.read_excel("C:/Users/wayne/mylinebot/vocabularybot/啟超的.xlsx")

        new_df = df.iloc[n]
        voclist = new_df.values.tolist()
        word = ""
        vocn = 1
        for v in voclist:
            word += f"{vocn}. {v[0]} \n解釋: {v[1]} \n例句: {v[2]} \n翻譯: {v[3]} \n \n"
            vocn += 1

        return word

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == "Hello bot ":
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text = "123"))
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = "請輸入 Hello bot ")
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()