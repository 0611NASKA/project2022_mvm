from playsound import playsound 
import simpleaudio

wav_obj = simpleaudio.WaveObject.from_wave_file("audio_0.wav")
play_obj = wav_obj.play()
play_obj.wait_done()