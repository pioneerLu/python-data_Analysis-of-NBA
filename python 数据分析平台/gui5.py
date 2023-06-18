import tkinter as tk
import subprocess

def start_spider():
    text_box.insert(tk.END, "正在爬取数据...\n")
    subprocess.call(["python", r"nba_players\Spider1.py"])
    result = subprocess.call(["python", r"nba_players\Spider1.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result == 0:
        text_box.insert(tk.END, "爬取成功\n")
    else:
        text_box.insert(tk.END, "爬取失败\n")

def generate_analysis():
    subprocess.Popen(["python", r"nba_players\PlayerRadarMap.py"])

root = tk.Tk()
root.title("单球员水平分析")
root.geometry("600x400")  # 设置窗口大小为600x400像素

button1 = tk.Button(root, text="获取数据", command=start_spider)
button1.pack()

button2 = tk.Button(root, text="生成分析图样", command=generate_analysis)
button2.pack()

text_box = tk.Text(root, height=10, width=50)
text_box.pack()

root.mainloop()
