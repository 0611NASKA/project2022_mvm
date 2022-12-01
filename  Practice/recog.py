import speech_recognition as sr  
import subprocess
import keyboard


def recognize():                                                           
  r = sr.Recognizer()
  with sr.Microphone() as source:  
      r.adjust_for_ambient_noise(source)                                                                     
      print("あかりちゃんへの質問を喋ってね:")                                                                                   
      audio = r.listen(source)   

  msg = ""

  try:
      msg = r.recognize_google(audio, language='ja-JP')
      print("-----------detect!----------\n", msg)
  except sr.UnknownValueError:
      print("Could not understand audio")
  except sr.RequestError as e:
      print("Could not request results; {0}".format(e))

  if msg != "":
    print("あなたが喋ったのは " + msg)
  else:
    print("聞き取れなかったみたいです...")

while True:
    if keyboard.read_key() == "space":
        recognize()



# if __name__ == "__main__":
#   main()
