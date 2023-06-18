from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import subprocess

def callback():
    print("让我们进入分析吧")

def pass_callback():
    correct_pwd = 'Gary030916'
    if pwd.get() == correct_pwd:
        print("验证通过！")
        root.destroy()
        gui2()  # 进入gui2模块
    else:
        print("验证失败！")

def gui2():
    def player_data():
        if comb.get() == 'players':
            players = pd.read_csv(r"C:\Users\Garylu\Desktop\python 数据分析平台\nba_players\score.csv", encoding='utf-8')
            subprocess.call(["python", "gui3.py"])  # 调用gui3文件
        elif comb.get() == 'teams':
            subprocess.call(["python", "gui4.py"])  # 调用gui4文件
        elif comb.get() == 'certain player':
            subprocess.call(["python", "gui5.py"])  # 调用gui5文件

    root1 = Tk()
    root1.title('这才是正经的分析界面')
    root1.geometry('1000x1000')
    root1.resizable(False, False)

    photo = Image.open("background.png")
    photo = photo.resize((600, 300))
    img0 = ImageTk.PhotoImage(photo)
    img1 = ttk.Label(root1, text="照片:", image=img0)
    img1.pack()

    lab2 = Label(root1, text="请选择想要分析/预测的数据", font=("黑体", 20, "bold"), pady=30)
    lab2.pack()

    comb = ttk.Combobox(root1, textvariable=StringVar(), values=['players', 'teams', 'certain player'])
    comb.pack()

    button = Button(root1, text="分析", command=player_data, width=10, height=1, compound='center', pady=10)
    button.pack()

    lab2 = Label(root1, text="欢迎进入NBA数据分析平台!", font=("黑体", 20, "bold"), pady=30)
    lab2.pack()

    mainloop()

root = Tk()
root.title("NBA软脚虾球员分析")
root.geometry("700x700")
root.resizable(False, False)

image = PhotoImage(file=r"C:\Users\Garylu\Desktop\python 数据分析平台\nba_players\NBA图片1.png")
lab1 = Label(root, image=image)
lab1.pack()

lab2 = Label(root, text="欢迎进入NBA数据分析平台!", font=("黑体", 20, "bold"), pady=30)
lab2.pack()

pwd = Entry(root, show="*")
pwd.pack()

pwd_txt = Label(root, font=('黑体', 10, "bold"), text="不知道密码也想分析??", pady=10)
pwd_txt.pack()

button = Button(root, text="start", command=pass_callback, width=10, height=1, compound='center', pady=10)
button.pack()

mainloop()
