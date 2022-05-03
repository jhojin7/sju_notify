import json

def json_read(file:str)->dict:
    with open(file,'r',encoding="utf-8") as f:
        data = json.loads(f.read())
        f.close()
        return data

def json_write(file:str,data:dict):
    f = open(file,'w')
    f.write(json.dumps(data,ensure_ascii=False,indent=4))
    f.close()

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