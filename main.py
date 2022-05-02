from datetime import datetime
import boards, notify, etc

DIR = '/home/pi/CODE/sju_notify'
LOG = f"log: {datetime.today()}\n"
boardNames = ['main','haksa','chuiup','janghak']
datajson = ''
data = etc.json_read(DIR+'/data.json')

# MAIN
if __name__ == '__main__':
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
            notify.alert(etc.make_message(notice))
        all_new_notices += new_notices

    log_append(DIR, LOG, all_new_notices)
    
    # alert(f"TEST: {datetime.datetime.today()}\nupdated {len(new_notices)} notices\n")
    etc.json_write(DIR+'/data.json',data)