import sys
import subprocess
from urllib import request
import requests
import json
import time
# msg_q="おはよう"
# APIをたたく
def synthesis(text, filename, speaker=1, max_retry=20):
    # Internal Server Error(500)が出ることがあるのでリトライする
    # （HTTPAdapterのretryはうまくいかなかったので独自実装）
    # connect timeoutは10秒、read timeoutは300秒に設定（処理が重いので長めにとっておく）
    # audio_query
    print("test")
    query_payload = {"text": text, "speaker": speaker}
    for query_i in range(max_retry):
        r = requests.post("http://localhost:50021/audio_query", 
                        params=query_payload, timeout=(10.0, 300.0))
        if r.status_code == 200:
            query_data = r.json()
            break
        time.sleep(1)
    else:
        raise ConnectionError("リトライ回数が上限に到達しました。 audio_query : ", filename, "/", text[:30], r.text)

    # synthesis
    synth_payload = {"speaker": speaker}    
    for synth_i in range(max_retry):
        r = requests.post("http://localhost:50021/synthesis", params=synth_payload, 
                          data=json.dumps(query_data), timeout=(10.0, 300.0))
        if r.status_code == 200:
            with open(filename, "wb") as fp:
                fp.write(r.content)
            print(f"{filename} は query={query_i+1}回, synthesis={synth_i+1}回のリトライで正常に保存されました")
            break
        time.sleep(1)
    else:
        raise ConnectionError("リトライ回数が上限に到達しました。 synthesis : ", filename, "/", text[:30], r,text)


def sendRequest(msg_q):
  msg_q="歌って"
  url = 'https://api-mebo.dev/api'

  item_data = {
    "api_key":"0b4f7780-dfe0-471c-b7d3-ffab716fd255184cc81f488390",
    "agent_id":"462e9809-f4ad-48cb-bd02-fced3b113cd7184cc4962d9309",
    "utterance":msg_q,
    "uid":"<YOUR-UID-HERE>"
  }

  return requests.post(url, headers={}, json=item_data)

def getAnswerMsg(msg_q):
  res = sendRequest(msg_q)

  res_json = res.json()
#   print(res.json())

  return res_json["bestResponse"]["utterance"]

# MAIN LOGIC
def main():
  PATH_TO_SEIKASAY2EXE = "C:\\hogefoobar\\assistantseika\\SeikaSay2\\SeikaSay2.exe"

  args = sys.argv

  # 第一引数をQとしておく
  request_msg = args[0]
  print("request_msg: " + request_msg)

  if request_msg != "":
    # 回答を用意する(とりあえずv1は外部APIを使う)
    response_msg = getAnswerMsg(request_msg)
    print("response_msg: " + response_msg)
    texts = [
        response_msg
    ]
    print("test")
    for i, t in enumerate(texts):
        synthesis(t, f"audio_{i}.wav")

if __name__ == "__main__":
  main()