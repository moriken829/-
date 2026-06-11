import streamlit as st
import pandas as pd

# アプリのタイトル
st.set_page_config(page_title="競馬予想AIツール", layout="wide")
st.title("🏇 競馬予想Webアプリ")

st.sidebar.header("レース情報の入力")

# 入力フォーム
def input_features():
    horse_name = st.sidebar.text_input("馬名", "サンプルホース")
    last_rank = st.sidebar.number_input("前走の着順", min_value=1, max_value=18, value=5)
    speed_index = st.sidebar.slider("スピード指数 (0-100)", 0, 100, 50)
    jockey_rank = st.sidebar.selectbox("騎手ランク", ["S (トップクラス)", "A (有力)", "B (普通)", "C (若手など)"])
    
    return {
        "馬名": horse_name,
        "前走着順": last_rank,
        "スピード指数": speed_index,
        "騎手ランク": jockey_rank
    }

# データ保持用（簡易版なのでメモリ上に保存）
if 'horses' not in st.session_state:
    st.session_state.horses = []

# 馬の追加ボタン
data = input_features()
if st.sidebar.button("この馬を追加"):
    # 簡易スコア計算ロジック
    score = data["スピード指数"]
    score += (18 - data["前走着順"]) * 2
    jockey_scores = {"S (トップクラス)": 20, "A (有力)": 10, "B (普通)": 5, "C (若手など)": 0}
    score += jockey_scores[data["騎手ランク"]]
    
    data["予想スコア"] = score
    st.session_state.horses.append(data)
    st.success(f"{data['馬名']} を追加しました！")

# 登録された馬の表示
if st.session_state.horses:
    st.subheader("📊 出走予定馬・予想結果")
    df = pd.DataFrame(st.session_state.horses)
    
    # スコア順にソート
    df = df.sort_values(by="予想スコア", ascending=False).reset_index(drop=True)
    
    # 印の付与
    def give_mark(index):
        if index == 0: return "◎ (本命)"
        if index == 1: return "○ (対抗)"
        if index == 2: return "▲ (単穴)"
        return "△ (連下)"
    
    df["印"] = [give_mark(i) for i in range(len(df))]
    
    # テーブル表示
    st.table(df[["印", "馬名", "予想スコア", "スピード指数", "前走着順", "騎手ランク"]])

    if st.button("リストをリセット"):
        st.session_state.horses = []
        st.rerun()
else:
    st.info("左側のサイドバーから馬の情報を入力して追加してください。")