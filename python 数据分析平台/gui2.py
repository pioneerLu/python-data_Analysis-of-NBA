import pandas as pd
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from nba_players import PlayerRadarMap,K_Means

def player_data():
    players = pd.read_csv(r"C:\Users\Garylu\Desktop\python 数据分析平台\nba_players\score.csv",encoding='utf-8')
    K_Means.display()

    
root1 = Tk()
root1.title('NBA软脚虾球员分析')
root1.geometry('700x700')
root1.resizable(False, False)
# PlayerRadarMap.display()

photo = Image.open(r"background.png")  
photo = photo.resize((600,300))  #规定图片大小
img0 = ImageTk.PhotoImage(photo)
img1 = ttk.Label(root1,text="照片:",image=img0)
img1.pack()

lab2=Label(root1,text="请选择想要分析/预测的数据",font=("黑体", 20, "bold"),pady=30)
lab2.pack()

comb = ttk.Combobox(root1,textvariable=StringVar(),values=['players','teams'])
comb.place(x=270,y=400)

# comb.bind('<<ComboboxSelected>>',func=)


lab2=Label(root1,text="欢迎进入NBA数据分析平台!",font=("黑体", 20, "bold"),pady=30)
mainloop()