import requests

# https://m.weibo.cn/detail/4839626148415893

"""
GET /comments/hotflow?id=4839626148415893&mid=4839626148415893&max_id_type=0 HTTP/2
Host: m.weibo.cn

User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
MWeibo-Pwa: 1
X-XSRF-TOKEN: 0a45bc
DNT: 1
Connection: keep-alive
Referer: https://m.weibo.cn/detail/4839626148415893
Cookie: _T_WM=16103729053; XSRF-TOKEN=0a45bc; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=oid%3D4839626148415893%26luicode%3D20000061%26lfid%3D4839626148415893%26uicode%3D20000061%26fid%3D4839626148415893; mweibo_short_token=af868cb21a
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Sec-GPC: 1
TE: trailers
"""

wid = "4839626148415893"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "MWeibo-Pwa": "1",
    "Connection": "keep-alive",
    "Referer": f"https://m.weibo.cn/detail/{wid}",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "TE": "trailers",
}
url1 = f"https://m.weibo.cn/statuses/extend?id={wid}"
url2 = f"https://m.weibo.cn/comments/hotflow?id={wid}&mid={wid}&max_id_type=0"


resp = requests.get(url2, headers=headers)
with open("comment-response.json", "w") as fh:
    import json

    json.dump(resp.json(), fh, ensure_ascii=False, indent=4)
