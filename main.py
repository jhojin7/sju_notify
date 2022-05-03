from datetime import datetime
import os
import boards, notify, etc

testdata_path = os.path.join(os.path.abspath(""),'tests','data.json')
LOG = f"log: {datetime.today()}\n"
# boardNames = ['main','haksa','chuiup','janghak']
boardIds = {
    333:"main",
    335:"haksa",
    337:"chuiup",
    338:"janghak"
}

# MAIN
if __name__ == '__main__':
    ### check for update
    for boardId in boardIds.keys():
        print("==", boardId, boardIds[boardId], "==")
        # TODO: DB도 해결해야함. sqlite3로할지 아니면 mongodb할지?
        new = boards.fetch_board(boardId)
        for _ in new: print(_)
        # send out notifications 
        for notice in new:
            notify.alert(notify.make_message(notice))
        # append to db
        db = etc.json_read(testdata_path)
        db[boardIds[boardId]] += new
        is_success = etc.json_write(testdata_path, db)
        if not is_success:
            print(">> !!!!!!!!! WRITE FAILED !!!!!!!!!")

    # etc.log_append(DIR, LOG, all_new_notices)
    
    # # alert(f"TEST: {datetime.datetime.today()}\nupdated {len(new_notices)} notices\n")
    # etc.json_write(DIR+'/data.json',data)