from main import *
from re import findall

HOME_SEJONG = "https://home.sejong.ac.kr/bbs/bbslist.do?bbsid=%s&wslID=%s"
HOME_SEJONG_VIEW = "https://home.sejong.ac.kr/bbs/bbsview.do?bbsid=%s&pkid=%s&wslID=%s"
BOARD_SEJONG = "https://board.sejong.ac.kr/boardlist.do?bbsConfigFK=%s"
BOARD_SEJONG_VIEW = "https://board.sejong.ac.kr/boardview.do?bbsConfigFK=%s&pkid=%s"

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
