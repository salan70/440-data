import pandas as pd
import sqlite3
import numpy as np

batting_csv_path = "assets/Lahman_1871-2023_data/lahman_1871-2023_csv/Batting.csv"
batting_scheme_file_path = "scheme/batting_stats.sql"
output_db_file_path = "output/batting_stats.db"

# SQLite データベースに接続 (存在しない場合は新規作成)
conn = sqlite3.connect(output_db_file_path)

# SQLファイルを実行してテーブルを作成
try:
    with open(batting_scheme_file_path, "r") as sql_file:
        conn.executescript(sql_file.read())
except FileNotFoundError:
    print(f"エラー: ファイル '{batting_scheme_file_path}' が見つかりません。")
    conn.close()
    exit(1)

# CSVファイルを読み込む
df = pd.read_csv(batting_csv_path, encoding="ISO-8859-1")

# カラム名のリネーム
df = df.rename(
    columns={
        "playerID": "playerId",
        "yearID": "year",
        "teamID": "teamId",
        "G": "G",
        "AB": "AB",
        "R": "R",
        "H": "H",
        "2B": "2B",
        "3B": "3B",
        "HR": "HR",
        "RBI": "RBI",
        "BB": "BB",
        "IBB": "IBB",
        "HBP": "HBP",
        "SO": "SO",
        "SB": "SB",
        "CS": "CS",
        "SH": "SAC",
        "SF": "SF",
        "GIDP": "GIDP",
    }
)

# * データの加工と計算

# displayOrder の計算
df["displayOrder"] = (
    df.sort_values(by=["year", "stint"]).groupby("playerId").cumcount() + 1
)

# PA の計算 (打席数)
df["PA"] = df["AB"] + df["BB"] + df["HBP"] + df["SAC"] + df["SF"]

# 長打数 XBH の計算
df["XBH"] = df["2B"] + df["3B"] + df["HR"]

# 塁打数 TB の計算
df["TB"] = df["H"] - df["XBH"] + 2 * df["2B"] + 3 * df["3B"] + 4 * df["HR"]

# 打率 AVG = H / AB
df["AVG"] = df["H"] / df["AB"]

# 出塁率 OBP = (H + BB + HBP) / (AB + BB + HBP + SF)
df["OBP"] = (df["H"] + df["BB"] + df["HBP"]) / (
    df["AB"] + df["BB"] + df["HBP"] + df["SF"]
)

# 長打率 SLG = (H + XBH) / AB
df["SLG"] = (df["H"] + df["XBH"]) / df["AB"]

# OPS = OBP + SLG
df["OPS"] = df["OBP"] + df["SLG"]

# ISO = SLG - AVG
df["ISO"] = df["SLG"] - df["AVG"]

# BABIP = (H - HR) / (AB - SO - HR + SF)
df["BABIP"] = (df["H"] - df["HR"]) / (df["AB"] - df["SO"] - df["HR"] + df["SF"])

# AB/HR = AB / HR
df["AB/HR"] = df["AB"] / df["HR"].replace(0, np.nan)  # HRが0の場合はNaNに置き換え

# BB/K = BB / SO
df["BB/K"] = df["BB"] / df["SO"].replace(0, np.nan)  # SOが0の場合はNaNに置き換え

# BB% = BB / PA
df["BB%"] = df["BB"] / df["PA"]

# SO% = SO / PA
df["SO%"] = df["SO"] / df["PA"]

# * 必要に応じて NaN を 0 に置き換え
# 整数型のカラムリスト
int_columns = ['G', 'PA', 'AB', 'H', 'XBH', 'TB', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 'IBB', 'HBP', 'SO', 'SB', 'CS', 'SAC', 'SF', 'GIDP']
# すべての整数型カラムに対して NaN を 0 に置き換え
df[int_columns] = df[int_columns].fillna(0).astype(int)

# * 不要なカラムを削除
df = df.drop(columns=["stint", "lgID", "G_batting", "G_old"])

# * データベースにデータを挿入
df.to_sql("BattingStats", conn, if_exists="append", index=False)

# 接続を閉じる
conn.close()
