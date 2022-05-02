import requests
from bs4 import BeautifulSoup
from re import findall
import etc

HOME_SEJONG = "https://home.sejong.ac.kr/bbs/bbslist.do?bbsid=%s&wslID=%s"
HOME_SEJONG_VIEW = "https://home.sejong.ac.kr/bbs/bbsview.do?bbsid=%s&pkid=%s&wslID=%s"
BOARD_SEJONG = "https://board.sejong.ac.kr/boardlist.do?bbsConfigFK=%s"
BOARD_SEJONG_VIEW = "https://board.sejong.ac.kr/boardview.do?bbsConfigFK=%s&pkid=%s"

def fetch_board(boardId:int):
    url = f"https://board.sejong.ac.kr/boardlist.do?bbsConfigFK={boardId}"
    # print(url)
    response = requests.get(url)
    soup =BeautifulSoup(response.text,'html.parser')
    return soup.find('table').find_all('tr')[1:] #remove head

def fetch_HOME_board(URL,boardId:int,wslID:str='xxx'):
    param = (str(boardId),wslID)
    response = requests.get(URL%param)
    print(response.url)
    soup =BeautifulSoup(response.text,'html.parser')
    rows = soup.find('table').find_all('tr')[1:] #remove head
    ret = []
    for row in rows:
        if row.find("등록된 게시물이 없습니다") != None:
            return "Finished"
        # fetch with HOME_SEJONG , boardid, and make_json on every item seen 
        ret.append(make_json(boardId,row))
    return ret

def make_SEJONG_view_link(boardId, pkid,*kwargs): ###########
    # print(TYPE, boardId, pkid)
    ret = BOARD_SEJONG_VIEW %(boardId,pkid)
    return ret

def make_HOME_view_link(boardId, pkid:str, wslID:str='xxx'):
    # print(TYPE, boardId, pkid)
    ret = HOME_SEJONG_VIEW %(boardId,pkid,wslID)
    return ret

def make_item(boardId, notice:str,wslID='cedpt')->dict:
    """ DUPLICATE. clean up later. """
    subject = notice.find('td','subject')
    subject_txt = subject.text.strip()
    writer = notice.find('td','writer').text.strip()
    date = notice.find('td','date').text.strip()
    index = notice.find('td','index').text.strip()
    a_href = subject.find('a').get('href')
    pkid = findall('pkid=([0-9]*)',a_href)[0]
    item = {
        "index":index,
        "subject":subject_txt,
        "writer":writer,
        "date":date,
        "pkid":pkid,
        "link":make_SEJONG_view_link(boardId,pkid,wslID)
    }
    return item

def check_for_update(boardName:str)-> list:
    """ DUPLICATE. clean up later. """
    global DIR, LOG
    old_data = etc.json_read(DIR+'/data.json')
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

def process(boardName:str, notices:list)->list:
    """ DUPLICATE. clean up later. """
    global DIR
    data = etc.json_read(DIR+'/data.json')
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