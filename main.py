# imports
import json
import requests
import datetime
from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter

# ONLY USED WHEN STARTING FROM SCRATCH
def init_json():
    # initialize data.json
    data = {
        "main":[],
        "haksa":[],
        "chuiup":[],
        "janghak":[],
        "boards2":{
            "main": 333,
            "haksa": 335,
            "chuiup": 337,
            "janghak": 338
        }
    }
    json_write('/home/pi/CODE/sju-notify/data.json',data)
    f = open('data.json','w')
    f.write(json.dumps(data,ensure_ascii=False,indent=4))
    f.close()

def fetch_board(boardId:int):
    url = f"https://board.sejong.ac.kr/boardlist.do?bbsConfigFK={boardId}"
    # print(url)
    response = requests.get(url)
    soup =BeautifulSoup(response.text,'html.parser')
    return soup.find('table').find_all('tr')[1:] #remove head

def json_read(file:str)->dict:
    f = open(file,'r')
    data = json.loads(f.read())
    f.close()
    return data

def json_write(file:str,data:dict):
    f = open(file,'w')
    f.write(json.dumps(data,ensure_ascii=False,indent=4))
    f.close()

def process(boardName:str, notices:list)->list:
    global DIR
    data = json_read(DIR+'/data.json')
    boardId = data['boards2'][boardName]
    # notices = fetch_board(boardId)

    tmp = []
    for notice in notices:
        subject = notice.find('td','subject')
        subject_txt = subject.text.strip()
        writer = notice.find('td','writer').text.strip()
        date = notice.find('td','date').text.strip()
        index = notice.find('td','index').text.strip()
        # print(index, subject_txt, writer, date)
        # link preprocessing
        link = subject.find('a').get('href')
        pkid = link[-6:]
        real_link = f"https://board.sejong.ac.kr/boardview.do?bbsConfigFK={boardId}&pkid={pkid}"
        notice = {
            "index":index,
            "subject":subject_txt,
            "writer":writer,
            "date":date,
            "pkid":pkid,
            "link":real_link
        }
        tmp.append(notice)
        # data[boardName].append(notice)    
    return tmp
    # json_write('data.json',data)

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

def check_for_update(boardName:str)-> list:
    global DIR, LOG
    old_data = json_read(DIR+'/data.json')
    boards = old_data['boards2']

    old = old_data[boardName]
    new = process(boardName,
        fetch_board(boards[boardName]))

    # scan for different post in new
    updated = []
    # search for only 5, for time complexity
    for i in range(5):
        if new[i] not in old:
            updated.append(new[i])
    if updated == []:
        LOG += f">>> {boardName}: scan complete. no diff\n"
    else:
        LOG += f">>> {boardName}: yes diff\n{updated}\n"
    return updated

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

# MAIN
if __name__ == '__main__':
    DIR = '/home/pi/CODE/sju_notify'
    LOG = f"log: {datetime.datetime.today()}\n"
    boardNames = ['main','haksa','chuiup','janghak']
    datajson = ''
    data = json_read(DIR+'/data.json')

    ### check for update
    all_new_notices = []
    for name in boardNames:
        new_notices = check_for_update(name)
        print(new_notices)
        data[name] += new_notices
        ### sort by pkid (oldest on top)
        data[name].sort(key=(lambda x: x['pkid']))

        ### alert new_notices
        for notice in new_notices:
            alert(make_message(notice))
        all_new_notices += new_notices

    log_f = open(DIR+'/log.txt','a')
    LOG += f"--- Updated {len(all_new_notices)} notices ---\n"
    log_f_lines = log_f.write(LOG)
    log_f.close()
    print(LOG)
    
    # alert(f"TEST: {datetime.datetime.today()}\nupdated {len(new_notices)} notices\n")
    json_write(DIR+'/data.json',data)