# coding=utf-8
"""\
Requirements:

wordcloud
matplotlib
requests
"""

import json
import matplotlib.pyplot as plt
import requests
import wordcloud

SCOREDB_API = "https://scoredb.tech/api.do/Students/NameList?\
sign=0766b2c89b5b7cc01e4b37147dabcd6f&time=1570800066&valid=7776000"
FONT_PATH = r"C:\Windows\Fonts\Deng.ttf"

if __name__ == '__main__':
    try:
        api_response = json.loads(requests.get(SCOREDB_API).content)  # 调用ScoreDB API获取所有同学的姓名
        if api_response["success"]:
            names_raw = api_response["data"]
        else:
            raise Exception("API request wasn't successful.")  # API调用失败的处理
    except Exception as e:
        print("Error: ", e)
        exit()
    else:
        text = []
        for name in names_raw:
            for char in name:
                text.append(char)
        text = " ".join(text)
        wc = wordcloud.WordCloud(width=1024, height=768,
                                 max_font_size=360,
                                 margin=3, regexp=r'\w+',  # 允许单字
                                 font_path=FONT_PATH)
        wc.generate(text)  # 生成词云
        plt.figure(figsize=(10.24, 7.68))  # 分辨率 1024 × 768
        plt.imshow(wc)
        plt.axis("off")
        plt.show()
