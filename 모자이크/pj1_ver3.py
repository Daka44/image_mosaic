import numpy as np
import cv2
from tkinter import *
from tkinter.filedialog import *
from PIL import ImageTk, Image
from tkinter import filedialog

window = Tk()
window.title("모자이크")
window.geometry("600x600")
file_path = ''

def Load():
    global file_path
    file_path = filedialog.askopenfilename()
    label1 = Label(window, text=file_path)
    label1.pack()  # 레이블을 윈도우에 배치
    print(file_path)


def save(image):
    image.save("수업\파이썬\프로젝트\모자이크\saved_image.jpg")

    # photo_image = ImageTk.PhotoImage(photo)
    # print(type(photo))
    # photo_image.save("saved_image.jpg")

    # photo.save("saved_image.jpg")  # 저장할 파일명 및 형식
    print("이미지가 저장되었습니다.")

def Mosaic(file_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # img = cv2.imread(file_path)
    img = np.fromfile(file_path, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)

    if img is None:
        print("이미지를 읽을 수 없습니다.")
    else:
        img = cv2.resize(img, dsize=(0,0), fx=1.0, fy=1.0, interpolation=cv2.INTER_LINEAR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 얼굴을 찾아 모자이크 처리
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            face_img = img[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, dsize=(0,0), fx=0.02, fy=0.02)
            face_img = cv2.resize(face_img, (w,h), interpolation=cv2.INTER_AREA)
            img[y:y+h, x:x+w] = face_img

        mosaic_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 색상 변환
        image = Image.fromarray(mosaic_img)
        image = image.resize((400, 400), Image.Resampling.LANCZOS)
        
        # print(type(image))
        photo = ImageTk.PhotoImage(image)

        label2 = Label(window, image=photo)
        label2.image = photo
        print(type(label2.image))
        label2.pack(anchor="center")
        

        btn_3 = Button(window, text="저장" , command=lambda: save(image))
        btn_3.place(x=550,y=550)



button_1 = Button(window, text="사진 불러오기", command=Load)
button_1.place(x=10, y=10)

button_2 = Button(window, text='모자이크 시작', command=lambda: Mosaic(file_path))
button_2.place(x=10, y=50)



window.mainloop()