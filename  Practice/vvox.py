import requests
import json
import time
print("test")
# VoicevoxでText to Speechするやつ
def synthesis(text, filename, speaker=4, max_retry=20):
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

def text_to_speech():
    # ※テキストはイメージです
    texts = [
        "私は倒れたものでなく立ち上がったものを称える",
        "こっちを探索しよう",
        "敵を確認",
        "自然の力を召喚する",
        "ダウンした。救援を"
    ]
    print("test")
    for i, t in enumerate(texts):
        synthesis(t, f"audio_{i}.wav")
if __name__ == '__main__':
    text_to_speech()