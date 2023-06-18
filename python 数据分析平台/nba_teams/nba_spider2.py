import requests
import re
import csv

class NBASpider:

    def __init__(self):
        # self.url = "https://www.basketball-reference.com/leagues/NBA_2016.html"
        self.url="https://www.basketball-reference.com/leagues/NBA_2022.html"
        self.schedule_url = "https://www.basketball-reference.com/leagues/NBA_2022_games-{}.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 "
                          "Safari/537.36"
        }

    # 发送请求，获取数据
    def send(self, url):
        response = requests.get(url, headers = self.headers)
        response.encoding = 'utf-8'
        return response.text

    # 解析html
    def parse(self, html):
        team_heads, team_datas = self.get_team_info(html)
        opponent_heads, opponent_datas = self.get_opponent_info(html)
        return team_heads, team_datas, opponent_heads, opponent_datas

    def get_team_info(self, html):
        """
        通过正则从获取到的html页面数据中team表的表头和各行数据
        :param html 爬取到的页面数据
        :return: team_heads表头
                 team_datas 列表内容
        """
        # 1. 正则匹配数据所在的table
        team_table = re.search('<table.*?id="per_game-team".*?>(.*?)</table>', html, re.S).group(1)
        # 2. 正则从table中匹配出表头
        team_head = re.search('<thead>(.*?)</thead>', team_table, re.S).group(1)
        team_heads = re.findall('<th.*?>(.*?)</th>', team_head, re.S)
        # 3. 正则从table中匹配出表的各行数据
        team_datas = self.get_datas(team_table)

        return team_heads, team_datas

    # 解析opponent数据
    def get_opponent_info(self, html):
        """
        通过正则从获取到的html页面数据中opponent表的表头和各行数据
        :param html 爬取到的页面数据
        :return:
        """
        # 1. 正则匹配数据所在的table
        opponent_table = re.search('<table.*?id="per_game-opponent".*?>(.*?)</table>', html, re.S).group(1)
        # 2. 正则从table中匹配出表头
        opponent_head = re.search('<thead>(.*?)</thead>', opponent_table, re.S).group(1)
        opponent_heads = re.findall('<th.*?>(.*?)</th>', opponent_head, re.S)
        # 3. 正则从table中匹配出表的各行数据
        opponent_datas = self.get_datas(opponent_table)

        return opponent_heads, opponent_datas

    # 获取表格body数据
    def get_datas(self, table_html):
        """
        从tboday数据中解析出实际数据（去掉页面标签）
        :param table_html 解析出来的table数据
        :return:
        """
        tboday = re.search('<tbody>(.*?)</tbody>', table_html, re.S).group(1)
        contents = re.findall('<tr.*?>(.*?)</tr>', tboday, re.S)
        for oc in contents:
            rk = re.findall('<th.*?>(.*?)</th>', oc)
            datas = re.findall('<td.*?>(.*?)</td>', oc, re.S)
            datas[0] = re.search('<a.*?>(.*?)</a>', datas[0]).group(1)
            datas = rk + datas
            # yield 声明这个方法是一个生成器， 返回的值是datas
            yield datas

    def get_schedule_datas(self, table_html):
        """
        从tboday数据中解析出实际数据（去掉页面标签）
        :param table_html 解析出来的table数据
        :return:
        """
        tboday = re.search('<tbody>(.*?)</tbody>', table_html, re.S).group(1)
        contents = re.findall('<tr.*?>(.*?)</tr>', tboday, re.S)
        for oc in contents:
            rk = re.findall('<th.*?><a.*?>(.*?)</a></th>', oc)
            datas = re.findall('<td.*?>(.*?)</td>', oc, re.S)
            if datas and len(datas) > 0:
                datas[1] = re.search('<a.*?>(.*?)</a>', datas[1]).group(1)
                datas[3] = re.search('<a.*?>(.*?)</a>', datas[3]).group(1)
                datas[5] = re.search('<a.*?>(.*?)</a>', datas[5]).group(1)

            datas = rk + datas
            # yield 声明这个方法是一个生成器， 返回的值是datas
            yield datas

    def parse_schedule_info(self, html):
        """
        通过正则从获取到的html页面数据中team表的表头和各行数据
        :param html 爬取到的页面数据
        :return: team_heads表头
                 team_datas 列表内容
        """
        # 1. 正则匹配数据所在的table
        table = re.search('<table.*?id="schedule" data-cols-to-freeze=",1">(.*?)</table>', html, re.S).group(1)
        table = table + "</tbody>"
        # 2. 正则从table中匹配出表头
        head = re.search('<thead>(.*?)</thead>', table, re.S).group(1)
        heads = re.findall('<th.*?>(.*?)</th>', head, re.S)
        # 3. 正则从table中匹配出表的各行数据
        datas = self.get_schedule_datas(table)

        return heads, datas

    # 存储成csv文件
    def save_csv(self, title, heads, rows):
        f = open(title + '.csv', mode='w', encoding='utf-8', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=heads)
        csv_writer.writeheader()
        for row in rows:
            dict = {}
            if heads and len(heads) > 0:
                for i, v in enumerate(heads):
                    dict[v] = row[i] if len(row) > i else ""
            csv_writer.writerow(dict)

    def crawl_team_opponent(self):
        # 1. 发送请求
        res = self.send(self.url)
        # 2. 解析数据
        team_heads, team_datas, opponent_heads, opponent_datas = self.parse(res)
        # 3. 保存数据为csv
        self.save_csv("team", team_heads, team_datas)
        self.save_csv("opponent", opponent_heads, opponent_datas)

    def crawl_schedule(self):
        months = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]
        for month in months:
            html = self.send(self.schedule_url.format(month))
            # print(html)
            heads, datas = self.parse_schedule_info(html)
            # 3. 保存数据为csv
            self.save_csv("schedule_"+month, heads, datas)

    def crawl(self):
        self.crawl_schedule()


if __name__ == '__main__':
    # 运行爬虫
    spider = NBASpider()
    spider.crawl()
