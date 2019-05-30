from tkinter import *
from collections import Counter
from random import choice
import time
import os
import sys

class tetris:
    collor=["blue","purple","orange","lightblue"]
    Box_size = 40
    width= Box_size * 8
    height= Box_size * 14
    Combo = 0
    ComboBox = []
    Score = 0
    

    for a in list(range(1,10)) :       # 이미지 파일 문자열 규칙 생성
        ComboBox.append([])
        word = "COMBO 0{num}_000".format(num = a)
        for b in list(range(1,33)) :
            if b <= 9 :
                word2 = word + "0" + str(b) + ".png"
            else :
                word2 = word + str(b) + ".png"

            ComboBox[a-1].append(word2)


    def __init__(self) :
        rows = int(tetris.height / tetris.Box_size)
        columns = int(tetris.width / tetris.Box_size)

        self.MyboxNum = []
        self.changed_boxNum = []
        self.temp_boxNum=[]
        self.chain_trigger = False
        self.limitedkey=0
        self.rotate=0
        self.speed=150
        self.gameover = "OFF"

        # 외곽선 맵 생성관련 논리
        for a in range(rows) :
            if a == 0 :
                for b in range(columns) :
                    canvas.create_rectangle(b * tetris.Box_size, 0, (b + 1) * tetris.Box_size, tetris.Box_size, fill = "gray", outline = "gray")

            if a == rows -1 :
                for b in range(columns) :
                    canvas.create_rectangle(b * tetris.Box_size, (tetris.Box_size * rows) - tetris.Box_size, (b + 1) * tetris.Box_size, tetris.Box_size * rows, fill = "gray", outline = "gray")

            canvas.create_rectangle(0, a * tetris.Box_size, tetris.Box_size, (a + 1) * tetris.Box_size, fill = "gray", outline = "gray")
            canvas.create_rectangle((columns - 1) * tetris.Box_size, a * tetris.Box_size, columns * tetris.Box_size , (a + 1) * tetris.Box_size, fill = "gray", outline = "gray")

        objBox = self.make_Box()
        self.objbox = objBox       # self.objbox == 현재 움직이고 있는 박스
        self.MyboxNum.append(self.objbox)

        objBox2= self.make_Box2()
        self.objbox2=objBox2
        self.MyboxNum.append(self.objbox2)


    # 박스 생성 이벤트
    def make_Box(self):
        make_box = canvas.create_rectangle(tetris.width / 2, 0, tetris.width / 2 + tetris.Box_size, tetris.Box_size, fill=choice(self.collor))
        return make_box

    def make_Box2(self):
        make_box = canvas.create_rectangle(tetris.width / 2 + tetris.Box_size, 0, tetris.width / 2 + tetris.Box_size*2, tetris.Box_size, fill=choice(self.collor))
        return make_box


    # 박스 fall 이벤트
    def fall(self, objBox):
        self.overlap()
        if self.BoxCoords[1] == 0:           
            canvas.move(objBox, 0, tetris.Box_size)

        elif self.can_fall :
            canvas.move(objBox, 0, tetris.Box_size/2)           
        self.overlap()

    def fall2(self, objBox):
        self.overlap2()
        if self.BoxCoords2[1] == 0:
            canvas.move(objBox, 0, tetris.Box_size)

        elif self.can_fall2 :
            canvas.move(objBox, 0, tetris.Box_size/2)
        self.overlap2()


    # 게임 조작키 이벤트
    def handle_events(self,event):
        if not self.gameover == "ON" :    # 게임오버 후 키입력을 제한
            if self.limitedkey!=1:   # 오버래핑이 발생한 경우 키입력을 제한
                self.overlap()
                self.overlap2()

                if (self.can_left or (self.can_left2 and self.rotate==2)) and (self.can_left2 or self.rotate!=1) :   
                    if event.keysym == "Left":
                        canvas.move(self.objbox, -tetris.Box_size, 0)
                    if event.keysym == "Left":
                        canvas.move(self.objbox2, -tetris.Box_size, 0)

                if (self.can_right2 or (self.can_right and self.rotate==2)) and (self.can_right or self.rotate!=3) :
                    if event.keysym == "Right":
                        canvas.move(self.objbox, tetris.Box_size, 0)
                    if event.keysym == "Right":
                        canvas.move(self.objbox2, tetris.Box_size, 0)

                
                if event.keysym == "Up" :
                    if self.rotate==3:
                        self.overlap()
                        if self.can_left or self.can_right:
                            if self.can_right==False:
                                canvas.move(self.objbox, -tetris.Box_size,0)
                                canvas.move(self.objbox2, -tetris.Box_size,0)
                            canvas.move(self.objbox2, tetris.Box_size, tetris.Box_size)
                            self.rotate=0
                    else:
                        if self.rotate==2:
                            canvas.move(self.objbox2, tetris.Box_size, -tetris.Box_size)
                            self.rotate=3
                        if self.rotate==1:
                            self.overlap2()
                            if self.can_left2 or self.can_right2:
                                if not self.can_left2:
                                    canvas.move(self.objbox, tetris.Box_size,0)
                                    canvas.move(self.objbox2, tetris.Box_size,0)
                                canvas.move(self.objbox2,-tetris.Box_size,-tetris.Box_size)
                                self.rotate=2
                        if self.rotate==0:
                            a=self.overlap3(self.objbox2)
                            if a==False:
                                canvas.move(self.objbox, 0, -tetris.Box_size)
                                canvas.move(self.objbox2, 0, -tetris.Box_size)
                                canvas.move(self.objbox2, -tetris.Box_size,tetris.Box_size)
                                self.rotate=1
                            else:
                                canvas.move(self.objbox2, -tetris.Box_size,tetris.Box_size)
                                self.rotate=1
                                
                if event.keysym=="Down":
                    self.overlap()
                    self.overlap2()
                    if self.can_fall and self.can_fall2:
                        canvas.move(self.objbox, 0, tetris.Box_size/2)
                        canvas.move(self.objbox2, 0, tetris.Box_size/2)

                self.overlap()
                self.overlap2()

    # 오버래핑 관련 함수
    def overlap(self):
        self.BoxCoords = canvas.coords(self.objbox)   # Boxcoords == [x1,y1,x2,y2]  / 현재 박스 좌표값 List
        if self.objbox != "Recreate" :
            overlap = [
                       canvas.find_overlapping(self.BoxCoords[0], self.BoxCoords[1] + 1, self.BoxCoords[0], self.BoxCoords[3] - 1),  # 왼쪽 선
                       canvas.find_overlapping(self.BoxCoords[2], self.BoxCoords[1] + 1, self.BoxCoords[2], self.BoxCoords[3] - 1),  # 오른쪽 선
                       canvas.find_overlapping(self.BoxCoords[0] + 1, self.BoxCoords[3], self.BoxCoords[2] - 1 , self.BoxCoords[3])  # 밑면 선
                      ]

            if len(overlap[0]) <= 1 :
                self.can_left = True
            else :
                self.can_left = False

            if len(overlap[1]) <= 1 :
                self.can_right = True
            else :
                self.can_right = False

            if len(overlap[2]) <= 1 :
                self.can_fall = True
            else :
                self.can_fall = False
                if self.rotate==1:      # rotate돼서 box2가 box1 밑으로 간 경우
                    self.can_fall= True
                    if self.can_fall2 == False:
                        self.can_fall=False

    def overlap2(self):
        self.BoxCoords2 = canvas.coords(self.objbox2)   # Boxcoords == [x1,y1,x2,y2]  / 현재 박스 좌표값 List
        if self.objbox2 != "Recreate" :
            overlap = [
                       canvas.find_overlapping(self.BoxCoords2[0], self.BoxCoords2[1] + 1, self.BoxCoords2[0], self.BoxCoords2[3] - 1),  # 왼쪽 선
                       canvas.find_overlapping(self.BoxCoords2[2], self.BoxCoords2[1] + 1, self.BoxCoords2[2], self.BoxCoords2[3] - 1),  # 오른쪽 선
                       canvas.find_overlapping(self.BoxCoords2[0] + 1, self.BoxCoords2[3], self.BoxCoords2[2] - 1 , self.BoxCoords2[3])  # 밑면 선
                      ]

            if len(overlap[0]) <= 1 :
                self.can_left2 = True
            else :
                self.can_left2 = False

            if len(overlap[1]) <= 1 :
                self.can_right2 = True
            else :
                self.can_right2 = False

            if len(overlap[2]) <= 1 :
                self.can_fall2 = True
            else :
                self.can_fall2 = False
                if self.rotate==3:      # rotate돼서 box가 box2 밑으로 간 경우
                    self.can_fall2= True
                    if self.can_fall == False:
                        self.can_fall2=False

    def overlap3(self,objbox):
        if self.rotate==0:
            Boxcoord3=canvas.coords(objbox)
            if not Boxcoord3==[]:
                overlap=canvas.find_overlapping(Boxcoord3[0] -tetris.Box_size + 1, Boxcoord3[3]+tetris.Box_size/2, Boxcoord3[2] -tetris.Box_size - 1 , Boxcoord3[3]+tetris.Box_size/2)
                if (int(len(overlap))>0):
                    return False
            return True

    # 연쇄 제거 함수
    def gravity(self) :                # MyboxNum = 박혀있는 상자  / changed_boxNum = 위치가 변경된 상자
        self.changed_boxNum = []   # gravity함수 시작전 gravity를 체험한 상자들의 값들을 초기화
        for _ in self.MyboxNum :
            BoxCoords = canvas.coords(_)
            overlap = canvas.find_overlapping(BoxCoords[0] + 1, BoxCoords[3], BoxCoords[2] - 1 , BoxCoords[3])  # MyboxNum 리스트에 등록된 상자들의 밑면선 오버랩을 실시
            if len(overlap) == 1 :
                self.changed_boxNum.append(_)  # 위치가 변경될 상자를 change_boxNum에 담음
                list(set(self.changed_boxNum))

            while len(overlap) == 1 :     # 위치를 변경 시킴
                canvas.move(str(_), 0, tetris.Box_size/2)
                canvas.update()
                BoxCoords = canvas.coords(_)
                overlap = canvas.find_overlapping(BoxCoords[0] + 1, BoxCoords[3], BoxCoords[2] - 1 , BoxCoords[3])

    # 게임 메인 루프
    def timer(self):
        if self.objbox == "Recreate" :  # 새로운 상자 생성
            self.objbox = self.make_Box()
            self.MyboxNum.append(self.objbox)       # 추가되는 상자번호 MyboxNum 리스트에 등록
            self.objbox2 = self.make_Box2()
            self.MyboxNum.append(self.objbox2)
            self.rotate=0
        
        bb.Combo = 0
        self.limitedkey=0
        self.ScoreBox = []  # 점수계산용 박스상자 생성
        self.fall(self.objbox)
        self.fall2(self.objbox2)  
        self.GameOver()

        
        if self.can_fall == False or self.can_fall2 ==False :  # 한 블록이 멈췄을 시 움직임 제한
            self.limitedkey=1
            self.speed=50
        if self.can_fall == False and self.can_fall2 ==False :
            self.speed=150
            if (self.rotate==1) :
                temp=self.MyboxNum.index(self.objbox)
                self.MyboxNum[temp]=self.objbox2
                self.MyboxNum[temp+1]=self.objbox
            canvas.update()
            time.sleep(0.1)
            a=self.popping(self.objbox)
            if(self.objbox2 in self.MyboxNum) :
                b=self.popping(self.objbox2)
            if (a or b) :
                bb.Combo += 1
                self.chain_trigger = True  # 점수 계산용 아직 미구현
                # self.Comboprint(self.x, self.y)
                self.gravity()
                while self.chain_trigger :  # 팝핑이 일어나면 반복
                    canvas.update()
                    time.sleep(0.1)
                    self.chain_trigger = False
                    self.temp_boxNum=self.changed_boxNum[:]  # 포문 리스트 변경 방지
                    for a in self.temp_boxNum :
                        if a in self.changed_boxNum :
                            k = self.popping(a)
                        if k :
                            self.chain_trigger = True
                            for b in list(self.removeNum) :
                                if b in self.changed_boxNum :
                                    self.changed_boxNum.remove(b)

                    if self.chain_trigger:
                        bb.Combo += 1
                        # self.Comboprint(self.x, self.y)
                    self.gravity()

            self.objbox = "Recreate"
            self.objbox2 = "Recreate"

        ScorePlus  = 10 * len(self.ScoreBox) * (2 ** (bb.Combo - 1))    # 점수계산 수식 = (팝핑된 상자갯수 X 10) X 2^(콤보수)
        bb.Score += int(ScorePlus)
        ScorePlus = 0
        status_var.set("Score: {}".format(bb.Score))

        canvas.after(self.speed,self.timer)


    def find_samecolor(self,a,samecolor,aleadyseen) :
        if a in aleadyseen :  # 이미 본 상자면 그대로 리턴
            return samecolor
        color = canvas.itemcget(a, "fill")
        coords = canvas.coords(a)
        lap=canvas.find_overlapping(coords[0],(coords[1]+coords[3])/2,coords[2],(coords[1]+coords[3])/2)  # 위 아래 오버랩
        lap2=canvas.find_overlapping((coords[0]+coords[2])/2,coords[1],(coords[0]+coords[2])/2,coords[3])  # 양 옆 오버랩
        lap=lap+lap2
        for i in lap :
            if(color==canvas.itemcget(i, "fill")) :
                samecolor.add(i)
        aleadyseen.add(a)
        temp=set([])
        for i in samecolor :
            temp.add(i)
        for i in temp:
            samecolor=self.find_samecolor(i,samecolor,aleadyseen)
        return samecolor

    def popping(self,a) :
        samecolor=set([])
        aleadyseen=set([])
        self.removeNum=self.find_samecolor(a,samecolor,aleadyseen)
        if(int(len(self.removeNum)) > 3) :
            self.x = canvas.coords(list(self.removeNum)[0])[0]   # x,y 좌표에 팝핑으로 삭제된 상자의 위치정보 저장
            self.y = canvas.coords(list(self.removeNum)[0])[1]
         
            for i in self.removeNum :
                color = canvas.itemcget(i, "fill")
                canvas.delete(i)
                self.MyboxNum.remove(i)   # 삭제된 상자번호 MyboxNum 리스트에서 제거
                self.ScoreBox.append(i)     # 삭제된 상자번호 ScoreBox 리스트에 등록 (점수계산용)
            return True
        return False

    def Comboprint(self, x, y) :
        count = 1
        Combo = bb.Combo - 1
        if Combo >= 8 :
            Combo = 8
        image = PhotoImage(file = bb.ComboBox[Combo][0]).subsample(4)
        for a in range(len(bb.ComboBox[0]))[::3] :
            if count == 1 :
                i = canvas.create_image(x, y,image = image)
            if count == 11 :
                canvas.delete(i)
                doon.update()
                break;

            image = PhotoImage(file = bb.ComboBox[Combo][a]).subsample(4)
            canvas.itemconfig(i,image = image)
            doon.update()
            count += 1

    def GameOver(self) :
        self.overlap()
        self.overlap2()
        
        if not self.can_fall or not self.can_fall2 :
            if self.BoxCoords[1] == bb.Box_size or self.BoxCoords2[1] == bb.Box_size :
                self.gameover = "ON"
                #GameOverimage = PhotoImage(file = "GameOver.png").subsample(4)
                #canvas.create_image(bb.Box_size * 4 + 10, bb.Box_size * 7, image = GameOverimage)
                #doon.update()         
                raise NotImplementedError
        else :
            return None

#os.chdir(sys._MEIPASS + '\image')

doon=Tk()
doon.title("PuyoPyuo Ver1.0")

canvas = Canvas(doon, width = tetris.width, height = tetris.height)
canvas.pack()

bb=tetris()
doon.bind("<Key>", bb.handle_events)


status_var = StringVar()
status_var.set("Score: {}".format(bb.Score))
status = Label(doon,
        textvariable=status_var,
        font=("Helvetica", 10, "bold"))
status.pack()

bb.timer()
doon.mainloop()
