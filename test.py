# 加载包
import itchat
import requests
import urllib.parse

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
   robotChat(msg)

def robotChat(msg):
    print('robot chat')
    print(msg['Text'])
    sendMsg = msg['Text'].strip()
    try:
        r = requests.get('https://www4.bing.com/socialagent/chat?q=' + sendMsg+'&anid=123456')#小冰接口
        try:
            r1= r.json()
            info = urllib.parse.unquote(r1['InstantMessage']['ReplyText'])
            print(info)
            itchat.send(info, toUserName = msg['FromUserName'])#发送回复消息
        except Exception as e2:
            print(e2)
    except Exception as e:
        print(e)

itchat.auto_login()
itchat.run()
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyspider