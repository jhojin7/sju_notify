from discord import Webhook, RequestsWebhookAdapter
from main import json_read

def make_message(obj:dict)->str:
    subject = obj['subject']
    date = obj['date']
    writer = obj['writer'] 
    link = obj['link']
    message =\
f"""새로운 공지가 도착했어요! ({writer}, {date}):
{subject}
{link}"""
    return message

def alert(message:str):
    global DIR
    # WEBHOOK
    config = json_read(DIR+'/config.json')
    id = config['webhookId']
    token = config['webhookToken']

    # send message
    try:
        webhook = Webhook.partial(id,token, adapter=RequestsWebhookAdapter())
        webhook.send(message,username='세종대 공지 알림')
    except Exception as e:
        print(e)