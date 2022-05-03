import json
import os

repo = os.path.abspath("/home/pi/CODE/sju_notify")
testdata_path = os.path.join(repo,'tests','data.json')
data_path = os.path.join(repo,'data.json')
testconfig_path = os.path.join(repo,'tests','config.json')
config_path = os.path.join(repo,'config.json')

DATA = data_path
CONFIG = config_path

def json_read(file:str)->dict:
    """ Read json data to file. 
    Returns dict if successful, False if not. """
    with open(file,'r',encoding="utf-8") as f:
        data = json.loads(f.read())
        f.close()
        return data
    return False

def json_write(file:str,data:dict)->bool:
    """ Write dict type data to file. 
    Returns True if write successful, False if not. """
    try:
        with open(file,'w',encoding="utf-8") as f:
            f.write(json.dumps(data,ensure_ascii=False,indent=4))
            f.close()
        return True
    except Exception as e:
        print(e)
        return False

def log_append(DIR, LOG, all_new_notices):
    log_f = open(DIR+'/log.txt','a')
    LOG += f"--- Updated {len(all_new_notices)} notices ---\n"
    log_f_lines = log_f.write(LOG)
    log_f.close()
    print(LOG)

def init_json():
    """ ONLY USED WHEN STARTING FROM SCRATCH """
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