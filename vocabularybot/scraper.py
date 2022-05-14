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
print(vocab.getVoc(123))