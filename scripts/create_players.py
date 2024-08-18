import csv
import sqlite3

import pandas as pd


def create_players_db(output_db_file_path: str) -> None:
    """
    打撃成績のDBを作成する
    """
    people_csv_path = "assets/Lahman_1871-2023_data/lahman_1871-2023_csv/People.csv"
    players_scheme_file_path = "scheme/players.sql"

    # SQLite データベースに接続 (存在しない場合は新規作成)
    conn = sqlite3.connect(output_db_file_path)

    # SQLファイルを実行してテーブルを作成
    with open(players_scheme_file_path, "r") as sql_file:
        conn.executescript(sql_file.read())

    df = _load_and_preprocess_data(people_csv_path)

    # データベースにデータを挿入
    df.to_sql("Players", conn, if_exists="append", index=False)

    # 接続を閉じる
    conn.close()


def _load_and_preprocess_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, encoding="ISO-8859-1")

    # カラム名のリネーム
    column_mapping = {"playerID": "playerId"}
    df = df.rename(columns=column_mapping)

    # playerId, nameFirst, nameLast のみを抽出
    df = df[["playerId", "nameFirst", "nameLast"]]
    return df
