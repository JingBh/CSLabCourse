# coding=utf-8
"""\
Requirements:

requests
beautifulsoup4
wordcloud
jieba
matplotlib
"""

import json
import os
import time

import bs4
import jieba
# import jieba.analyse
import matplotlib.font_manager
import matplotlib.pyplot as plt
import requests
from wordcloud import WordCloud, STOPWORDS

FONT_PATH = r"C:\Windows\Fonts\Deng.ttf"
BASE_URL = "http://www.qhfz.edu.cn"
LIST_URL = BASE_URL + "/xiaonaxinwen/list_70_%s.html"
USER_AGENT = "Mozilla/5.0 JWS/1.0 (like Chrome) from THSCSLab"
HEADERS = {
    "User-Agent": USER_AGENT
}

DATA_DIR = os.path.realpath(os.path.dirname(__file__) + "/data")
DATA_FILE = os.path.realpath(DATA_DIR + "/qhfz_news.json")

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def get_cache():
    if os.path.exists(DATA_FILE):
        try:
            handler = open(DATA_FILE, "r", encoding="utf-8")
            cache = handler.read()
            handler.close()
            return json.loads(cache)
        except Exception:
            pass
    return None


def write_cache(content):
    handler = open(DATA_FILE, "w", encoding="utf-8")
    handler.write(json.dumps(content))
    handler.close()


def get_articles_list():
    result = []
    fail = 0
    page = 1
    time_min = time.time() - 2592000  # 一个月
    while True:
        url = LIST_URL % page
        print("[Info] Requesting URL:", url)
        try:
            list_request = requests.get(url, HEADERS)
            list_request.raise_for_status()
            list_html = list_request.content.decode()
            list_soup = bs4.BeautifulSoup(list_html, "html.parser")
            list_ele = list_soup.select("ul.gwlist2")[0]
            for ele in list_ele.contents:
                if type(ele) == bs4.Tag:
                    link_ele = ele.select("a")[0]
                    date_ele = ele.select("span")[0]
                    if time.mktime(time.strptime(date_ele.text, "%Y-%m-%d")) < time_min:
                        return result
                    else:
                        result.append(link_ele.attrs["href"])
            page += 1
        except Exception as e:
            print("[Error]", e, "\n[Info] Retrying...")
            fail += 1
            if fail > 10:
                print("[Error] Failed to get contents.")
                return None


def get_content():
    cache = get_cache()
    if cache is None:
        result = {}
        articles_list = get_articles_list()
        for link in articles_list:
            fail = 0
            url = BASE_URL + link
            print("[Info] Requesting URL:", url)
            while True:
                try:
                    request = requests.get(url, HEADERS)
                    request.raise_for_status()
                    html = request.content.decode()
                    soup = bs4.BeautifulSoup(html, "html.parser")
                    title = None
                    content = ""
                    for i in soup.select(".con")[0].contents:
                        try:
                            classes = i.attrs["class"]
                            if "position" in classes:
                                continue
                            elif "tit" in classes:
                                title = i.text
                                continue
                        except Exception:
                            pass
                        if type(i) == bs4.Tag:
                            content += i.text
                        else:
                            content += i
                    content = content.replace("\n", "").replace("\r", "").replace(" ", "")
                    if title is not None:
                        result[title] = content
                    break
                except Exception as e:
                    print("[Error]", e, "\n[Info] Retrying...")
                    fail += 1
                    if fail > 3:
                        print("[Error] Failed to get contents of \"%s\"." % url)
                        break
        write_cache(result)
        print("[Info] Contents fetched successfully.")
        return result
    else:
        return cache


if __name__ == '__main__':
    data = get_content()
    text = ""
    for title in data:
        text += data[title] + "\n"
    text_cut = " ".join(jieba.cut(text))
    # textrank = jieba.analyse.textrank(text_cut, topK=100, withWeight=True)
    # keywords = {}
    # for i in textrank:
    #     keywords[i[0]] = i[1]
    stop_words = STOPWORDS | {"end", "\n", "\r",
                              "审核", "图文", "编辑", "时间",
                              "来源", "作者", "点击", "次",
                              "的", "了"}
    wc = WordCloud(font_path=FONT_PATH,
                   width=1000, height=1000,
                   max_font_size=360,
                   stopwords=stop_words)
    wc.generate(text_cut)
    # wc.generate_from_frequencies(keywords)
    plt_font = matplotlib.font_manager.FontProperties(fname=FONT_PATH, size=36)
    plt.figure(figsize=(10, 10.36))
    plt.imshow(wc)
    plt.title("清华附中网站近一个月新闻用词频率", fontproperties=plt_font)
    plt.axis("off")
    plt.show()
