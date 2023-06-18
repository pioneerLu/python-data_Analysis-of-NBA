import pandas as pd
import math
import numpy as np
import csv
from sklearn import linear_model
from sklearn.model_selection import cross_val_score

init_elo = 1600 # 初始化elo值
team_elos = {}
folder = r'C:\Users\Garylu\Desktop\python 数据分析平台\nba_teams'  # 文件路径

def PruneData(M_stat, O_stat, T_stat):
    #这个函数要完成的任务在于将原始读入的诸多队伍的数据经过修剪，使其变为一个以team为索引的排列的特征数据
    #丢弃与球队实力无关的统计量
    pruneM = M_stat.drop(['Rk', 'Arena'],axis = 1)
    pruneO = O_stat.drop(['Rk','G','MP'],axis = 1)
    pruneT = T_stat.drop(['Rk','G','MP'],axis = 1)
    
    #将多个数据通过相同的index：team合并为一个数据
    mergeMO = pd.merge(pruneM, pruneO, how = 'left', on = 'Team')
    newstat = pd.merge(mergeMO, pruneT,  how = 'left', on = 'Team')
    
    #将team作为index的数据返回
    return newstat.set_index('Team', drop = True, append = False)

def GetElo(team):
    # 初始化每个球队的elo等级分
    try:
        return team_elos[team]
    except:
        team_elos[team] = init_elo
    return team_elos[team]

def CalcElo(winteam, loseteam):
    # winteam, loseteam的输入应为字符串
    # 给出当前两个队伍的elo分数
    R1 = GetElo(winteam)
    R2 = GetElo(loseteam)
    # 计算比赛后的等级分，参考elo计算公式
    E1 = 1/(1 + math.pow(10,(R2 - R1)/400))
    E2 = 1/(1 + math.pow(10,(R1 - R2)/400))
    if R1>=2400:
        K=16
    elif R1<=2100:
        K=32
    else:
        K=24
    R1new = round(R1 + K*(1 - E1))
    R2new = round(R2 + K*(0 - E2))
    return R1new, R2new

def GenerateTrainData(stat, trainresult):
    #将输入构造为[[team1特征，team2特征]，...[]...]
    X = []
    y = []
    for index, rows in trainresult.iterrows():
        winteam = rows['WTeam']
        loseteam = rows['LTeam']
        #获取最初的elo或是每个队伍最初的elo值
        winelo = GetElo(winteam)
        loseelo = GetElo(loseteam)
        # 给主场比赛的队伍加上100的elo值
        if rows['WLoc'] == 'H':
            winelo = winelo+100
        else:
            loseelo = loseelo+100
        # 把elo当为评价每个队伍的第一个特征值
        fea_win = [winelo]
        fea_lose = [loseelo]
        # 添加我们从basketball reference.com获得的每个队伍的统计信息
        for key, value in stat.loc[winteam].iteritems():
            fea_win.append(value)
        for key, value in stat.loc[loseteam].iteritems():
            fea_lose.append(value)
        # 将两支队伍的特征值随机的分配在每场比赛数据的左右两侧
        # 并将对应的0/1赋给y值        
        if np.random.random() > 0.5:
            X.append(fea_win+fea_lose)
            y.append(0)
        else:
            X.append(fea_lose+fea_win)
            y.append(1)
        # 更新team elo分数
        win_new_score, lose_new_score = CalcElo(winteam, loseteam)
        team_elos[winteam] = win_new_score
        team_elos[loseteam] = lose_new_score
    # nan_to_num(x)是使用0代替数组x中的nan元素，使用有限的数字代替inf元素
    return np.nan_to_num(X),y
        
def GeneratePredictData(stat,info):
    X=[]
    #遍历所有的待预测数据，将数据变换为特征形式
    for index, rows in stat.iterrows():
        
        #首先将elo作为第一个特征
        team1 = rows['Vteam']
        team2 = rows['Hteam']
        elo_team1 = GetElo(team1)
        elo_team2 = GetElo(team2)
        fea1 = [elo_team1]
        fea2 = [elo_team2+100]
        #球队统计信息作为剩余特征
        for key, value in info.loc[team1].iteritems():
            fea1.append(value)
        for key, value in info.loc[team2].iteritems():
            fea2.append(value)
        #两队特征拼接
        X.append(fea1 + fea2)
    #nan_to_num的作用：1将列表变换为array，2.去除X中的非数字，保证训练器读入不出问题
    return np.nan_to_num(X)

if __name__ == '__main__':
    # 设置导入数据表格文件的地址并读入数据
    M_stat = pd.read_csv(folder + '/15-16Miscellaneous_Stat.csv')
    O_stat = pd.read_csv(folder + '/15-16Opponent_Per_Game_Stat.csv')
    T_stat = pd.read_csv(folder + '/15-16Team_Per_Game_Stat.csv')
    team_result = pd.read_csv(folder + '/2015-2016_result.csv')
    
    teamstat = PruneData(M_stat, O_stat, T_stat)
    X,y = GenerateTrainData(teamstat, team_result)

    # 训练网格模型
    limodel = linear_model.LogisticRegression()
    limodel.fit(X,y)

    # 10折交叉验证
    # print(cross_val_score(model, X, y, cv=10, scoring='accuracy', n_jobs=-1).mean())

    # 预测
    pre_data = pd.read_csv(folder + '/16-17Schedule.csv')
    pre_X = GeneratePredictData(pre_data, teamstat)
    pre_y = limodel.predict_proba(pre_X)
    predictlist = []
    for index, rows in pre_data.iterrows():
        reslt = [rows['Vteam'], pre_y[index][0], rows['Hteam'], pre_y[index][1]]
        predictlist.append(reslt)
    
    # 将预测结果输出保存为csv文件
    with open(folder+'/prediction.csv', 'w',newline='') as f:
        writers = csv.writer(f)
        writers.writerow(['Visit Team', 'corresponding probability of winning', 'Home Team', 'corresponding probability of winning'])
        writers.writerows(predictlist)