import itchat

import requests

import re

# jieba分词

import jieba

# wordcloud词云

import matplotlib.pyplot as plt

# from wordcloud import WordCloud, ImageColorGenerator

import os

import numpy as np

import PIL.Image as Image

from Include.wechat.chatUseData import DataUtil

import time

import schedule

import threading

import _thread



dataUtil = DataUtil()

class WeChat():



    def login(self):

        itchat.auto_login(hotReload=True)  # 登录，会下载二维码给手机扫描登录，hotReload设置为True表示以后自动登录

        itchat.run()  # 让itchat一直运行



    def getFriend(self, name):

        friends = itchat.search_friends(name = name)  # 获取微信好友列表，如果设置update=True将从服务器刷新列表

        userName = friends[0]['UserName']

        return userName



    def getFriends(self):

        friends = itchat.get_friends(update=True)[0:]

        return friends



    def getRoom(self, name):

        rooms = itchat.search_chatrooms(name=name)  # 获取微信群列表，如果设置update=True将从服务器刷新列表

        if rooms:

            userName = rooms[0]['UserName']

            return userName



    def getRooms(self):

        rooms = itchat.get_chatrooms(update=True)

        return rooms



    def ratio(self, friends):

        # 初始化计数器，有男有女，当然，有些人是不填的

        male = female = other = 0



        # 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算

        # 1表示男性，2女性

        for i in friends[1:]:

            sex = i["Sex"]

            if sex == 1:

                male += 1

            elif sex == 2:

                female += 1

            else:

                other += 1



        # 总数算上，好计算比例啊～

        total = len(friends[1:])

        # 好了，打印结果

        print(u"男性好友：%.2f%%" % (float(male) / total * 100))

        print(u"女性好友：%.2f%%" % (float(female) / total * 100))

        print(u"其他：%.2f%%" % (float(other) / total * 100))



    # def signature(self, friends):
    #
    #     tList = []
    #
    #     for i in friends:
    #
    #         signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
    #
    #         rep = re.compile("1f\d.+")
    #
    #         signature = rep.sub("", signature)
    #
    #         tList.append(signature)
    #
    #     text = "".join(tList)
    #
    #     wordlist_jieba = jieba.cut(text, cut_all=True)
    #
    #     wl_space_split = " ".join(wordlist_jieba)
    #
    #
    #
    #     d = os.path.dirname(__file__)
    #
    #     alice_coloring = np.array(Image.open(os.path.join(d, "wechat1.png")))
    #
    #     my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
    #
    #                              max_font_size=50, random_state=42,width=1000,height=860,
    #
    #                              font_path='C:/Windows/Fonts/STFANGSO.ttf').generate(wl_space_split)
    #
    #
    #
    #     image_colors = ImageColorGenerator(alice_coloring)
    #
    #     plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    #
    #     plt.imshow(my_wordcloud)
    #
    #     plt.axis("off")
    #
    #     plt.show()
    #
    #     my_wordcloud.to_file(os.path.join(d, "wechat_cloud.png"))
    #




    def sendMessage(self, message, name):

        itchat.send(message, toUserName=name)



    # 推送睡前故事

    def readStory(self):

        print('readStory do')

        # stroy = dataUtil.getBookInfo('./从你的全世界路过.txt')

        stroy = dataUtil.getBookInfo('./送你一颗子弹.txt')

        dataUtil.getBingPhoto('0')

        yfei = wechat.getFriend('方铭玮')



        for txt in stroy:

            wechat.sendMessage(txt, yfei)

            # wechat.sendMessage(txt, 'filehelper')



        itchat.send_image('./bing.jpg', toUserName=yfei)

        # itchat.send_image('./bing.jpg', 'filehelper')



        # itchat.send_file('./Passing through your world.mp3', toUserName=yfei)

        # group2 = wechat.getRoom('(￣(●●)￣)')

        # wechat.sendMessage(stroy, group2)



    # 推送每日早报

    def dailyInfo(self):

        print('dailyInfo do')

        jiujiang = dataUtil.getWeatherData('杭州')

        # wechat.sendMessage(jiujiang, 'filehelper')

        yfei = wechat.getFriend('方铭玮')

        wechat.sendMessage(jiujiang, yfei)

        # group2 = wechat.getRoom('幸福一家人')

        # wechat.sendMessage(hangz, group2)

        # group1 = wechat.getRoom('阿里A3研发部')

        # wechat.sendMessage(hangz, group1)



    # qinghua

    def qinghua(self):

        print('qinghua do')

        dailyMessage = dataUtil.getDaily()

        yfei = wechat.getFriend('方铭玮')

        wechat.sendMessage(dailyMessage, yfei)



    # 闹钟

    def alarm(self):

        print('alarm do')

        alarms = "小可爱，快到八点了！"

        yfei = wechat.getFriend('方铭玮')

        wechat.sendMessage(alarms, yfei)





# 历史信息

KEY = '71f9d9d2dd364ad8b28bd56527470176'

# 聊天助手开关

OPEN_FLAG = 0

# 回复信息

# @itchat.msg_register(['Text'])

def text_reply(msg):

    global OPEN_FLAG

    msgText = msg['Text']

    # print(msgText)

    if msgText == "小冰过来":

        OPEN_FLAG = 1

        print('开启小冰语音助手*')

        return '开启小冰语音助手*'

    if msgText == "小冰退下":

        OPEN_FLAG = 0

        print('关闭小冰语音助手*')

        return '关闭小冰语音助手*'

    if OPEN_FLAG == 1:

        # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复

        defaultReply = '不想说话了！' + "*"

        # 如果图灵Key出现问题，那么reply将会是None

        reply = get_response(msg['Text']) + "*"

        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试

        return reply or defaultReply



KEY = '71f9d9d2dd364ad8b28bd56527470176'

# 图灵机器人

def get_response(msg):

    # 构造了要发送给服务器的数据

    apiUrl = 'http://www.tuling123.com/openapi/api'

    data = {

        'key': KEY,

        'info': msg,

        'userid': 'wechat-robot',

    }

    try:

        r = requests.post(apiUrl, data=data).json()

        return r.get('text')

    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常

    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return

    except Exception as e:

        print('插入时发生异常' + e)

        # 将会返回一个None

        return





wechat = WeChat() #这里是封装的 itchat

# 开启微信登录线程，需要单独占个线程

_thread.start_new_thread(wechat.login, ( ))



# 配置定时任务

# 开启早间天气预报 定时任务

schedule.every().day.at("7:00").do(wechat.dailyInfo)

# 开启每日一句 定时任务

schedule.every().day.at("20:00").do(wechat.qinghua)

# 开启睡前故事 定时任务

schedule.every().day.at("21:30").do(wechat.readStory)

while True:

    schedule.run_pending()

    time.sleep(1)




