from urllib import request
import requests
import json
msg_q="おやすみ"
# APIをたたく
def sendRequest(msg_q):
  url = 'https://api-mebo.dev/api'

  item_data = {
    "api_key":"f913984a-5200-4d05-b299-2c6e72f136c2184615a01781c1",
    "agent_id":"0ee8a82d-d64e-4c87-aab8-f40f4ff63de8182b18b7f8714e",
    "utterance":msg_q,
    "uid":"<YOUR-UID-HERE>"
  }

  return requests.post(url, headers={}, json=item_data)

# Answerをいい感じに捌く
def getAnswerMsg(msg_q):
  res = sendRequest(msg_q)
  print(res)
  res_json = res.json()

  print(res.json())
  print(res.json['bestResponse'])

  return res_json["bestResponse"]["utterance"]
if __name__ == '__main__':
    
    getAnswerMsg(msg_q)