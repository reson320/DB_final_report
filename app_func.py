# 此檔須放在gui.py資料夾下面的 /subdir/app_func.py 才可運行，沒有subdir請自行創
from operator import index
import psycopg2
import bs4
from bs4 import BeautifulSoup
from sympy import false  # 導入BeautifulSoup
import re # regular expression
import pandas as pd
import tkinter as tk
import sys
import tabulate

def askurl(urlbase): # used for web crawler
    import urllib.request
    #simulate header and send request to web, then GET data
    header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept-Language":"en-US,en;q=0.9"
    }
    request = urllib.request.Request(urlbase,headers=header)

    try:
        response = urllib.request.urlopen(request,timeout=5)
        html = response.read().decode("utf-8")
    except Exception as a:
        print(a)
    return html

def update_DB():
    conn = psycopg2.connect(
        database="postgres",
        user="Ray",
        password="aaa",
        host="database-1.cnsjnjwcvkcd.us-east-1.rds.amazonaws.com",
        port='5432'
    )
    conn.autocommit = True

    positions = {"top", "jungle", "mid", "adc", "support"} #預設牌位白金
    regions = {"NA","EUW","KR"}
    for reg in regions:
        for pos in positions:
            url = "http://www.op.gg/champions?position="+pos+"&region="+reg

            #delete old data
            try:
                table_name = reg+"_"+pos
                cur = conn.cursor()
                delstr="DELETE FROM {}".format(table_name)
                cur.execute(delstr)
            except Exception as e:
                print("Database connection failed due to {}".format(e))

            # 獲取html資訊
            html = askurl(url)
            # 解析數據
            soup = BeautifulSoup(html,"html.parser")

            name = []       #empty list to save data
            tier = []
            winRate = []
            pickRate = []
            banRate = []
                
            # 看tbody的所有children
            for tr in soup.find(name = "tbody").children:
                # 判斷tr是否為tag，去除空行
                if isinstance(tr,bs4.element.Tag):
                    # 查找tr tag下的td tag
                    tds = tr('td')

                    # 英雄名 (爬下來的資料是用字典序由小到大排)
                    tmp=tds[1].find('a').find('strong').string.split('\'')
                    nm=""
                    for tp in tmp:
                        nm+=tp
                    name.append(nm)

                    # tier
                    tir=re.search(r'\>\d\<',str(tds[2])).group()
                    tier.append(int(tir[1]))

                    # win rate
                    WR=re.search(r'\d+\.\d+',str(tds[3])).group()
                    winRate.append(float(WR))

                    # pick rate
                    PR=re.search(r'\d+\.\d+',str(tds[4])).group()
                    pickRate.append(float(PR))

                    # ban rate
                    BR=re.search(r'\d+\.\d+',str(tds[5])).group()
                    banRate.append(float(BR))
                    #insert new data
                    cur.execute("INSERT INTO {}(champion_name, tier, winrate, pickrate, banrate) VALUES (\'{}\',{},{},{},{})".format(table_name,name[-1],tier[-1],winRate[-1],pickRate[-1],banRate[-1]))

def recm(pos, cho, txt):
    conn = psycopg2.connect(
        database="postgres",
        user="Ray",
        password="aaa",
        host="database-1.cnsjnjwcvkcd.us-east-1.rds.amazonaws.com",
        port='5432'
    )
    # output dataframe to GUI
    txt.pack()
    class PrintTXT(object):
        def write(self, s):
            txt.insert(tk.END, s)
    sys.stdout = PrintTXT()

    nm=[]
    if cho=="1":
        try:
            cur = conn.cursor()
            exe_str="select a.champion_name,(a.tier+b.tier*2+c.tier) as total_tier,(a.winrate+b.winrate+c.winrate)/3 as avg_winrate from euw_{0} as a ,kr_{1} as b ,na_{2} as c where a.champion_name = b.champion_name and a.champion_name = c.champion_name order by total_tier asc,avg_winrate desc limit 5".format(pos,pos,pos)
            cur.execute(exe_str)
            query_results = cur.fetchall()
            for qr in query_results:
                nm.append(qr[0])
            df1 = pd.DataFrame(data=[nm], index=["Name"])
            df1 = pd.DataFrame(df1.values.T, columns=df1.index)
            print(pos)
            print(df1.to_markdown())
        except Exception as e:
            print("Database connection failed due to {}".format(e))
    else:
        cur = conn.cursor()
        exe_str="select a.champion_name,(a.tier+b.tier*2+c.tier) as total_tier,(a.winrate+b.winrate+c.winrate)/3 as avg_winrate from euw_{0} as a ,kr_{1} as b ,na_{2} as c where a.champion_name = b.champion_name and a.champion_name = c.champion_name order by total_tier asc,avg_winrate desc".format(pos,pos,pos)
        cur.execute(exe_str)
        query_results = cur.fetchall()
        tier=[]
        wr=[]
        for qr in query_results:
            nm.append(qr[0])
            tier.append(str(qr[1]))
            wr.append(round(qr[2],2))
        df = pd.DataFrame(data=[nm, tier, wr], index=["Name", "Tier", "Win Rate"])
        df2 = pd.DataFrame(df.values.T, columns=df.index)
        print(pos)
        print(df2.to_markdown())