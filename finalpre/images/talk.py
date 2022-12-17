from pygame.locals import *
import pygame
import sys
import random
import sys
import subprocess
from urllib import request
import requests
import json
import time
import speech_recognition as sr 
from playsound import playsound 
import simpleaudio
import keyboard

def sendRequest(msg_q):
#   msg_q = "こんにちは"
  r = sr.Recognizer()
  with sr.Microphone() as source:  
      r.adjust_for_ambient_noise(source)                                                                     
      print("何か話しかけてください:")                                                                                   
      audio = r.listen(source)   

  # msg_q = ""

  # try:
      msg_q = r.recognize_google(audio, language='ja-JP')
      print("-----------detect!----------\n", msg_q)
  # except sr.UnknownValueError:
  #     print("Could not understand audio")
  # except sr.RequestError as e:
  #     print("Could not request results; {0}".format(e))

  if msg_q != "":
    print("あなたが喋ったのは " + msg_q)
  else:
    print("聞き取れなかったみたいです...")

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
        # time.sleep(1)
    else:
        raise ConnectionError("リトライ回数が上限に到達しました。 synthesis : ", filename, "/", text[:30], r,text)




# MAIN LOGIC
def main1():
  PATH_TO_SEIKASAY2EXE = "C:\\hogefoobar\\assistantseika\\SeikaSay2\\SeikaSay2.exe"
  args = sys.argv
    
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
        time.sleep(1)
        
        wav_obj = simpleaudio.WaveObject.from_wave_file("audio_0.wav")
        play_obj = wav_obj.play()
        play_obj.wait_done()

def main():
    gamescene = 0  # 0 タイトル、1 ゲーム中、2 ゲームオーバー、-1 エラー
    pygame.init()  # Pygameを初期化
    screen = pygame.display.set_mode((900, 600))  # 画面を作成
    pygame.display.set_caption("My Voice Mate-Kuma")

    gamebutton = []
    gamebuttonrect = Rect(0, 0, 900, 600) # 画像の表示位置を表す矩形
    # gamebutton.append(pygame.image.load("./images/sleep.png"))
    # gamebutton.append(pygame.image.load("./images/regular.png"))
    # gamebutton.append(pygame.image.load("./images/angry.png"))
    img1 = pygame.image.load("./images/sleep.png")
    img2 = pygame.image.load("./images/regular.png")
    img3 = pygame.image.load("./images/speak.png")
    img1 = pygame.transform.scale(img1, (800, 600))
    img2 = pygame.transform.scale(img2, (800, 600))
    img3 = pygame.transform.scale(img3, (800, 600))
    gamebutton.append(img1)
    gamebutton.append(img2)
    gamebutton.append(img3)

    running = True
    # メインループ

    while running:
        screen.fill((100, 100, 100))  # 背景色で塗る
        # この時点では、　screen.blit(gamebutton[gamescene], gamebuttonrect) で済むけど、
        # とりあえずは、if文でわけておく
        if gamescene == 0:
            screen.blit(gamebutton[0], gamebuttonrect)
        elif gamescene == 1:
            screen.blit(gamebutton[1], gamebuttonrect)
        elif gamescene ==2:
            screen.blit(gamebutton[2], gamebuttonrect)
        else:
            print("error")

        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()  # pygameのウィンドウを閉じる
                sys.exit()  # システム終了
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if gamebuttonrect.collidepoint(event.pos):
                    if gamescene == 0:
                        gamescene = 1
                    elif gamescene == 1:
                        gamescene = 2
                        # main1()
                        PATH_TO_SEIKASAY2EXE = "C:\\hogefoobar\\assistantseika\\SeikaSay2\\SeikaSay2.exe"
                        args = sys.argv
    
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
                          gamescene = 2
                          for i, t in enumerate(texts):
                              synthesis(t, f"audio_{i}.wav")
                              time.sleep(1)
                          gamescene = 2
                          wav_obj = simpleaudio.WaveObject.from_wave_file("audio_0.wav")
                          gamescene = 2
                          screen.blit(gamebutton[2], gamebuttonrect)
                          pygame.display.update()  # 描画処理を実行
                          play_obj = wav_obj.play()
                          play_obj.wait_done()
                        gamescene = 2
                    elif gamescene == 2:
                        gamescene = 0
                    else:
                        gamescene = -1

        pygame.display.update()  # 描画処理を実行


if __name__ == "__main__":
    main()