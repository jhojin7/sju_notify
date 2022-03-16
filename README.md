# SJU-notify

세종대 공지 알리미 in Discord  

> 매 정시마다 전체공지, 학사공지, 취업공지, 장학공지 게시판을 확인하여 새로운 공지가 있으면 알려줍니다. 

## Setup
1. (디스코드에서) 서버설정 -> 연동 -> 웹후크 -> '새 웹후크' 클릭
2. 이름, 채널을 적절히 설정하기
3. '웹후크 URL 복사'클릭
(`https://discord.com/api/webhooks/...` 포맷으로 된 URL)
4. `main.py`와 같은 폴더에 `config.json`파일을 만든다
5. 아까 복사한 링크에서 webhookID와 webhookToken을 찾아서 
config.json에 추가한다.  
`.../webhooks/<your webhook ID here>/<your webhook token here>`

## `data.json` structure
```json
{
    "main":[
        {
            "index": "0000",
            "subject":"제목",
            "writer":"작성자",
            "date":"0000.00.00",
            "link":"https://board.sejong.ac.kr/..."
        },
        //...
    ],
    "haksa":[
        {
            "index": "0000",
            "subject":"제목",
            "writer":"작성자",
            "date":"0000.00.00",
            "link":"https://board.sejong.ac.kr/..."
        },
        //...
    ],
    "chuiup":[
        {
            "index": "0000",
            "subject":"제목",
            "writer":"작성자",
            "date":"0000.00.00",
            "link":"https://board.sejong.ac.kr/..."
        }, 
        //...
    ],
    "janghak":[
        {
            "index": "", // WARNING!! 장학공지는 index가 없음!!
            "subject":"제목",
            "writer":"작성자",
            "date":"0000.00.00",
            "link":"https://board.sejong.ac.kr/..."
        },
        //...
    ],
    "boards2":{
        "main": 333,
        "haksa": 335,
        "chuiup": 337,
        "janghak": 338
    }
}
```

## `config.json`
```json
{
    "webhookId":"<your webhook ID here>",
    "webhookToken":"<your webhook token here>"
}
```
## Resources
- discord.py: https://github.com/Rapptz/discord.py
    - Quickstart: https://discordpy.readthedocs.io/en/stable/quickstart.html
    - webhooks: https://discordpy.readthedocs.io/en/stable/api.html?highlight=webhook#webhook-support


## TODO
- [ ] 이전에 쓰던 private repo는 archive처리하기
- [ ] divide files
- [ ] 변수명 통일, 정리하기
- [ ] channel webhook말고 bot으로 푸시 메시지 구현
- [ ] cron with relative path