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
    voclist = []     # 獲選單字清單
    quizAns = []     # 測驗解答
    validQuiz = []   # 候選題目

    def getVoc(): # 從資料庫隨機抽取五個單字並格式化輸出
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
            word += f'{vocn}. {vocab.voclist[v][0]} \n解釋: {vocab.voclist[v][1]} \n例句: {vocab.voclist[v][2]} \n翻譯: {vocab.voclist[v][3]} \n \n'
            vocab.voclist[v].append(vocn)
            vocn += 1
        word += f'輸入"quiz"開始小測驗\n'

        for v in vocab.voclist:
            vocab.validQuiz.append(v)
        return word

    def getQuiz(): # 從獲選單字隨機不重複出題
        import random
        if len(vocab.validQuiz) > 0:
            quiz = random.choice(vocab.validQuiz)
            vocab.quizAns = quiz[-1]
        else:
            output = "沒有題目了"

        if len(vocab.validQuiz) > 0:
            output = f"{quiz[-2]} \n  a. {vocab.voclist[0][0]} \n  b. {vocab.voclist[1][0]} \n  c. {vocab.voclist[2][0]} \n  d. {vocab.voclist[3][0]} \n  e. {vocab.voclist[4][0]}"
            vocab.validQuiz.remove(quiz)

        return output

    def getAns():  # 判斷輸入答案是否正確
        if isinstance(event, MessageEvent):
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

@csrf_exempt
def callback(request):
    allowWords = ["今日單字", "quiz", "結束", "yes", "no", "a", "b", "c", "d", "e"]
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if event.message.text == "今日單字":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='今日單字',
                                text = "請選擇功能",
                                actions=[
                                    PostbackTemplateAction(
                                        label='推薦五個單字',
                                        data='data_vocab'
                                    ),
                                    PostbackTemplateAction(
                                        label='結束',
                                        data='data_break'
                                    )
                                ]
                            )
                        )
                    )
                if event.message.text not in allowWords:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='請輸入"今日單字"以獲得推薦單字')
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
                if (event.message.text == "quiz") or (event.message.text == "quiz "):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=vocab.getQuiz())
                    )
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