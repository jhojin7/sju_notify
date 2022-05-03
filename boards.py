import requests
from bs4 import BeautifulSoup
from re import findall
import os, etc

testdata_path = os.path.join(os.path.abspath(""),'tests','data.json')
data_path = os.path.join(os.path.abspath(""),'data.json')
DATA = data_path
boardIds = {
    333:"main",
    335:"haksa",
    337:"chuiup",
    338:"janghak"
}

HOME_SEJONG = "https://home.sejong.ac.kr/bbs/bbslist.do?bbsid=%s&wslID=%s"
HOME_SEJONG_VIEW = "https://home.sejong.ac.kr/bbs/bbsview.do?bbsid=%s&pkid=%s&wslID=%s"
BOARD_SEJONG = "https://board.sejong.ac.kr/boardlist.do?bbsConfigFK=%s"
BOARD_SEJONG_VIEW = "https://board.sejong.ac.kr/boardview.do?bbsConfigFK=%s&pkid=%s"

def tr_to_dict(boardId, notice)->dict:
    """ Use soup.find to turn <tr> to dict """
    subject = notice.find('td','subject')
    subject_txt = subject.text.strip()
    writer = notice.find('td','writer').text.strip()
    date = notice.find('td','date').text.strip()
    index = notice.find('td','index').text.strip()
    link = subject.find('a').get('href')
    pkid = link[-6:]
    real_link = f"https://board.sejong.ac.kr/boardview.do?bbsConfigFK={boardId}&pkid={pkid}"
    notice = {
        "boardId":boardId,
        "index":index,
        "subject":subject_txt,
        "writer":writer,
        "date":date,
        "pkid":pkid,
        "link":real_link
    }
    return notice

def fetch_board(boardId:int):
    fetched = []
    # board to fetch
    url = f"https://board.sejong.ac.kr/boardlist.do?bbsConfigFK={boardId}"
    response = requests.get(url)
    soup =BeautifulSoup(response.text,'html.parser')
    # get all <tr> on first page only
    rows = soup.find('table').find_all('tr')[1:]
    for row in rows:
        # process text in <tr> and append to fetched
        rowdata = tr_to_dict(boardId, row)
        # filter out if duplicates exist in db
        if not is_duplicate(boardId, rowdata):
            fetched.append(rowdata)
    return fetched

def is_duplicate(boardId, rowdata):
    board = etc.json_read(DATA)[boardIds[boardId]]
    for x in board:
        # if is duplicate under this condition, return true
        if x['subject']==rowdata['subject']\
        and x['writer']==rowdata['writer']\
        and x['date']==rowdata['date']\
        and x['pkid']==rowdata['pkid']:
            # print(x['index'], x['pkid'], x['subject'][:20])
            return True
    # if no match, return false
    return False

def fetch_HOME_board(URL,boardId:int,wslID:str='xxx'):
    param = (str(boardId),wslID)
    response = requests.get(URL%param)
    print(response.url)
    soup =BeautifulSoup(response.text,'html.parser')
    rows = soup.find('table').find_all('tr')[1:] #remove head
    ret = []
    for row in rows:
        if row.find("등록된 게시물이 없습니다") == None:
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

if __name__=='__main__':
    data = fetch_board(333)
    for d in data: print(d)