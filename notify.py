from discord import Webhook, RequestsWebhookAdapter
import os
import etc
testconfig_path = os.path.join(os.path.abspath(""),'tests','config.json')
config_path = os.path.join(os.path.abspath(""),'config.json')
CONFIG = config_path

boardKRnames= {
    333:"공지",
    335:"학사",
    337:"취업",
    338:"장학"
}

def make_message(obj:dict)->str:
    boardId = obj['boardId']
    subject = obj['subject']
    date = obj['date']
    writer = obj['writer'] 
    link = obj['link']
    message =\
f"""[{boardKRnames[boardId]}]// 새로운 공지가 도착했어요! ({writer}, {date}):
{subject}
{link}"""
    return message

def alert(message:str):
    # WEBHOOK
    config = etc.json_read(CONFIG)
    id = config['webhookId']
    token = config['webhookToken']
    # id = config['webhookId_local']
    # token = config['webhookToken_local']
    # send message
    try:
        webhook = Webhook.partial(id,token, adapter=RequestsWebhookAdapter())
        webhook.send(message,username='세종대 공지 알림')
        print(f">> alert: {message}")
    except Exception as e:
        print(e)