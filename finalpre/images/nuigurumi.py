from pygame.locals import *
import pygame
import sys
import random
import serial
import time
ser=serial.Serial('/dev/cu.usbmodem142301', 9600, timeout=1)


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
    img4 = pygame.image.load("./images/angry.png")
    img1 = pygame.transform.scale(img1, (800, 600))
    img2 = pygame.transform.scale(img2, (800, 600))
    img3 = pygame.transform.scale(img3, (800, 600))
    img4 = pygame.transform.scale(img4, (800, 600))
    gamebutton.append(img1)
    gamebutton.append(img2)
    gamebutton.append(img3)
    gamebutton.append(img4)
    running = True
    # メインループ

    while running:
        line = ser.readline()   # 行終端まで読み込む
        line = line.rstrip()
        print(line)
        screen.fill((100, 100, 100))  # 背景色で塗る

        # この時点では、　screen.blit(gamebutton[gamescene], gamebuttonrect) で済むけど、
        # とりあえずは、if文でわけておく
        if gamescene == 0:
            screen.blit(gamebutton[0], gamebuttonrect)
        elif gamescene == 1:
            screen.blit(gamebutton[1], gamebuttonrect)
        elif gamescene ==2:
            screen.blit(gamebutton[2], gamebuttonrect)
        elif gamescene ==3:
            screen.blit(gamebutton[3], gamebuttonrect)
        elif gamescene ==4:
            screen.blit(gamebutton[4], gamebuttonrect)
        else:
            print("error")

        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()  # pygameのウィンドウを閉じる
                sys.exit()  # システム終了
        if (line == b'1'):
                gamescene = 1
                
        if (line == b'2'):
            gamescene = 3
            
        if (line == b'3'):
            gamescene = 0


        pygame.display.update()  # 描画処理を実行


if __name__ == "__main__":
    main()