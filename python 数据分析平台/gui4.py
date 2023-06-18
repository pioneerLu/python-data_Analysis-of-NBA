import tkinter as tk
import subprocess

def run_spider1():
    subprocess.call(["python", r"nba_teams\nba_spider.py"])
    output_text.insert(tk.END, '该数据爬取完成\n')

def run_spider2():
    subprocess.call(['python', r'nba_teams\nba_spider2.py'])
    output_text.insert(tk.END, '该数据爬取完成\n')

def run_spider3():
    subprocess.call(['python', r'nba_teams\nba_spider3.py'])
    output_text.insert(tk.END, '该数据爬取完成\n')

def run_prediction():
    subprocess.call(['python', r'nba_teams\NBA.py'])
    output_text.insert(tk.END, '生成成功\n')

root = tk.Tk()
root.title('NBA Spider')

# 创建按钮
button1 = tk.Button(root, text='执行nba_spider.py', command=run_spider1)
button1.pack(pady=10)

button2 = tk.Button(root, text='执行nba_spider2.py', command=run_spider2)
button2.pack(pady=10)

button3 = tk.Button(root, text='执行nba_spider3.py', command=run_spider3)
button3.pack(pady=10)

button_prediction = tk.Button(root, text='生成预测结果', command=run_prediction)
button_prediction.pack(pady=10)

# 创建文本框
output_text = tk.Text(root, height=10, width=40)
output_text.pack(pady=10)

root.mainloop()
