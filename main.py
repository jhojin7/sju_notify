from datetime import datetime
import boards, notify, etc

boardIds = {
    333:"main",
    335:"haksa",
    337:"chuiup",
    338:"janghak"
}

# MAIN
if __name__ == '__main__':
    print(datetime.today())
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
        db = etc.json_read(etc.DATA)
        db[boardIds[boardId]] += new
        is_success = etc.json_write(etc.DATA, db)
        if not is_success:
            print(">> !!!!!!!!! WRITE FAILED !!!!!!!!!")