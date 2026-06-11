import pandas as pd
import time
import requests
from io import StringIO

# 宝塚記念 過去10年分のレースIDリスト
takarazuka_ids = [
    "202309030811", # 2023年
    "202209040811", # 2022年
    "202109030411", # 2021年
    "202009030811", # 2020年
    "201909030811", # 2019年
    "201809030811", # 2018年
    "201709030811", # 2017年
    "201609030811", # 2016年
    "201509030811", # 2015年
    "201409030811"  # 2014年
]

def get_takarazuka_data():
    all_results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("⏳ 宝塚記念10年分のデータを収集中...")
    
    for race_id in takarazuka_ids:
        year = race_id[:4]
        url = f"https://db.netkeiba.com/race/{race_id}"
        
        try:
            res = requests.get(url, headers=headers)
            res.encoding = 'EUC-JP'
            df = pd.read_html(StringIO(res.text))[0]
            
            df['開催年'] = year
            all_results.append(df)
            print(f"✅ {year}年のデータを取得しました")
            time.sleep(1) # サーバーへの優しさ
            
        except:
            print(f"❌ {year}年の取得に失敗しました")
            
    return pd.concat(all_results)

# 実行
df_takarazuka = get_takarazuka_data()

# 保存
df_takarazuka.to_csv("takarazuka_10years.csv", index=False, encoding="utf-8-sig")
print("\n✨ 完了！左のフォルダから 'takarazuka_10years.csv' をダウンロードしてください。")
