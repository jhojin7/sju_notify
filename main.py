from datetime import datetime
import os
import boards#, notify, etc

testdata_path = os.path.join(os.path.abspath(""),'tests','data.json')
# DIR = '/home/pi/CODE/sju_notify'
DIR = "."
LOG = f"log: {datetime.today()}\n"
# boardNames = ['main','haksa','chuiup','janghak']
datajson = ''
# data = etc.json_read(DIR+'/data.json')
boardIds = {
    333:"main",
    335:"haksa",
    337:"chuiup",
    338:"janghak"
}

# MAIN
if __name__ == '__main__':
    ### check for update
    all_new_notices = []
    for boardId in boardIds.keys():
        print("==", boardId, boardIds[boardId], "==")
        # TODO: DB도 해결해야함. sqlite3로할지 아니면 mongodb할지?
        new = boards.fetch_board(boardId)
        for _ in new: print(_)
        # data[name] += new_notices
        # ### sort by pkid (oldest on top)
        # data[name].sort(key=(lambda x: x['pkid']))


        # ### alert new_notices
        # for notice in new_notices:
        #     notify.alert(etc.make_message(notice))
        # all_new_notices += new_notices

    # etc.log_append(DIR, LOG, all_new_notices)
    
    # # alert(f"TEST: {datetime.datetime.today()}\nupdated {len(new_notices)} notices\n")
    # etc.json_write(DIR+'/data.json',data)