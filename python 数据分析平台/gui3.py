import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from nba_players import GetPlayerScore
players = pd.read_csv(r"nba_players\score.csv",encoding='utf-8')
kmeans = KMeans(n_clusters = 2)
X = preprocessing.minmax_scale(players[['得分','罚球命中率','命中率','三分命中率']])
# 将数组转换为数据框
X = pd.DataFrame(X, columns=['得分','罚球命中率','命中率','三分命中率'])
kmeans.fit(X)
players['cluster'] = kmeans.labels_
def display():
   
    res0Series = pd.Series(kmeans.labels_)
    res0 = res0Series[res0Series.values == 0]
    output_text.insert(tk.END, "Cluster 1:\n")
    output_text.insert(tk.END, str(players.iloc[res0.index]) + "\n\n")

    res1Series = pd.Series(kmeans.labels_)
    res1 = res1Series[res1Series.values == 1]
    output_text.insert(tk.END, "Cluster 2:\n")
    output_text.insert(tk.END, str(players.iloc[res1.index]) + "\n\n")


def k_SSE(X, clusters):
    K = range(1, clusters+1)
    TSSE = []
    for k in K:
        SSE = []
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_
        for label in set(labels):
            SSE.append(np.sum((X.loc[labels == label,] - centers[label, :])**2))
        TSSE.append(np.sum(SSE))

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('ggplot')
    plt.plot(K, TSSE, 'b*-')
    plt.xlabel('球员类型的个数')
    plt.ylabel('簇内离差平方和之和')
    plt.show()


def k_silhouette(X, clusters):
    K = range(2, clusters+1)
    S = []
    for k in K:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        labels = kmeans.labels_
        S.append(silhouette_score(X, labels, metric='euclidean'))

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('ggplot')
    plt.plot(K, S, 'b*-')
    plt.xlabel('球星类型数量')
    plt.ylabel('轮廓系数/划分明显程度')
    plt.show()


def process_data():
    players = pd.read_csv("nba_players/score.csv", encoding='utf-8')

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    sns.lmplot(x='得分', y='命中率', data=players,
               fit_reg=False, scatter_kws={'alpha': 0.8, 'color': 'steelblue'})
    plt.show()

    X = preprocessing.minmax_scale(
        players[['得分', '罚球命中率', '命中率', '三分命中率']])
    X = pd.DataFrame(X, columns=['得分', '罚球命中率', '命中率', '三分命中率'])
    k_SSE(X, 15)

    k_silhouette(X, 10)

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X)
    players['cluster'] = kmeans.labels_
    centers = []
    for i in players.cluster.unique():
        centers.append(players.loc[players.cluster == i, [
            '得分', '罚球命中率', '命中率', '三分命中率']].mean())
    centers = np.array(centers)

    sns.lmplot(x='得分', y='命中率', hue='cluster', data=players, markers=['^', 's'],
               fit_reg=False, scatter_kws={'alpha': 0.8}, legend=False)
    plt.scatter(centers[:, 0], centers[:, 2], c='k', marker='*', s=180)
    plt.xlabel('得分')
    plt.ylabel('命中率')
    plt.show()

    display()


def start_crawling():
    GetPlayerScore.spi()
    output_text.insert(tk.END, "数据爬取完成！\n")


window = tk.Tk()
window.title("NBA Players Clustering")
window.geometry("800x600")

process_button = tk.Button(window, text="Process Data", command=process_data)
start_button = tk.Button(window, text="开始爬取数据", command=start_crawling)

output_text = scrolledtext.ScrolledText(window, width=100, height=30)

process_button.pack(side=tk.LEFT, padx=10)
start_button.pack(side=tk.LEFT, padx=10)
output_text.pack(pady=10)

window.mainloop()
