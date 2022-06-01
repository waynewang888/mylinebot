class vocab():
    voclist = []
    quizAns = []
    def getVoc():
        import os
        from django.conf import settings
        import openpyxl
        file_ = "C:/Users/wayne/mylinebot/voc_with_blank.xlsx"
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
        else:
            output = "沒有題目了"
        return output


print(vocab.getVoc())
print(vocab.getQuiz())
print(vocab.voclist)