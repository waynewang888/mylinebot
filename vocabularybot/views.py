import random

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

class vocab():
    voclist = []
    quizAns = []
    def getVoc():
        import os
        from django.conf import settings
        import openpyxl
        file_ = "./voc_with_blank.xlsx"
        import pandas as pd
        import random
        n = []
        while len(n) < 5:
            num = random.randrange(716)
            if num not in n:
                n.append(num)
        df = pd.read_excel(file_)

        new_df = df.iloc[n]
        vocab.voclist = new_df.values.tolist()
        word = ""
        vocn = 1
        for v in range(len(vocab.voclist)):
            word += f"{vocn}. {vocab.voclist[v][0]} \n解釋: {vocab.voclist[v][1]} \n例句: {vocab.voclist[v][2]} \n翻譯: {vocab.voclist[v][3]} \n \n"
            vocab.voclist[v].append(vocn)
            vocn += 1

        return word

    def getQuiz():
        import random
        quiz = random.choice(vocab.voclist)
        vocab.quizAns = quiz[-1]

        if len(vocab.voclist) != 0:
            output = f"{quiz[-2]} \n  a. {vocab.voclist[0][0]} \n  b. {vocab.voclist[1][0]} \n  c. {vocab.voclist[2][0]} \n  d. {vocab.voclist[3][0]} \n  e. {vocab.voclist[4][0]}"
            vocab.voclist.remove(quiz)
        else:
            output = "沒有題目了"
        return output

@csrf_exempt
def callback(request):
    allowWords = ["今日單字", "vocab", "結束", "yes", "no", "a", "b", "c", "d", "e"]
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
                if event.message.text == "今日單字":
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='今日單字',
                                text = "請選擇功能",
                                actions=[
                                    PostbackTemplateAction(
                                        label='推薦五個單字',
                                        text='vocab',
                                        data='data_vocab'
                                    ),
                                    PostbackTemplateAction(
                                        label='結束',
                                        text='結束',
                                        data='data_break'
                                    )
                                ]
                            )
                        )
                    )
                elif event.message.text not in allowWords:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text='請輸入 "今日單字" 以獲得單字 ')
                    )
            if isinstance(event, PostbackEvent):
                if event.postback.data == 'data_vocab':
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=vocab.getVoc())
                    )
                elif event.postback.data == 'data_break':
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='bye')
                    )
            if isinstance(event, MessageEvent):
                if event.message.text == "vocab":
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='今日單字',
                                text="是否進行測驗",
                                actions=[
                                    PostbackTemplateAction(
                                        label='是',
                                        text='yes',
                                        data='data_yes'
                                    ),
                                    PostbackTemplateAction(
                                        label='否',
                                        text='no',
                                        data='data_no'
                                    )
                                ]
                            )
                        )
                    )
            if isinstance(event, PostbackEvent):
                if event.postback.data == 'data_yes':
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=vocab.getQuiz())
                    )
                elif event.postback.data == 'data_no':
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='bye')
                    )
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == "a":
                    if vocab.quizAns == 1:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='答對了')
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=f'正確答案是{chr(96 + vocab.quizAns)}，下次記得喔')
                        )
                elif event.message.text == "b":
                    if vocab.quizAns == 2:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='答對了')
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=f'正確答案是{chr(96 + vocab.quizAns)}，下次記得喔')
                        )
                elif event.message.text == "c":
                    if vocab.quizAns == 3:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='答對了')
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=f'正確答案是{chr(96 + vocab.quizAns)}，下次記得喔')
                        )
                elif event.message.text == "d":
                    if vocab.quizAns == 4:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='答對了')
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=f'正確答案是{chr(96 + vocab.quizAns)}，下次記得喔')
                        )
                elif event.message.text == "e":
                    if vocab.quizAns == 5:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='答對了')
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=f'正確答案是{chr(96 + vocab.quizAns)}，下次記得喔')
                        )












        return HttpResponse()
    else:
        return HttpResponseBadRequest()