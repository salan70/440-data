import pandas as pd
import sqlite3
import numpy as np


def create_batting_stats_db(output_dir_path: str) -> None:
    """
    打撃成績のDBを作成する
    """
    batting_csv_path = "assets/Lahman_1871-2023_data/lahman_1871-2023_csv/Batting.csv"
    batting_scheme_file_path = "scheme/batting_stats.sql"
    output_db_file_path = f"{output_dir_path}/batting_stats.db"

    # SQLite データベースに接続 (存在しない場合は新規作成)
    conn = sqlite3.connect(output_db_file_path)

    # SQLファイルを実行してテーブルを作成
    with open(batting_scheme_file_path, "r") as sql_file:
        conn.executescript(sql_file.read())

    df = _load_and_preprocess_data(batting_csv_path)

    # データベースにデータを挿入
    df.to_sql("BattingStats", conn, if_exists="append", index=False)

    # 接続を閉じる
    conn.close()


def _load_and_preprocess_data(batting_csv_path: str) -> pd.DataFrame:
    """
    CSVファイルを読み込み、データを加工する
    """
    # CSVファイルを読み込む
    df = pd.read_csv(batting_csv_path, encoding="ISO-8859-1")

    # カラム名のリネーム
    df = _rename_columns(df)

    # データの加工と計算を実行
    df = _process_and_calculate_data(df)

    # NaN を 0 に置き換える
    df = _replace_nan_with_zero(df)

    # 不要なカラムを削除
    df = df.drop(columns=["stint", "lgID", "G_batting", "G_old"])

    return df


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    データフレームのカラム名をリネームする
    """
    column_mapping = {
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
    return df.rename(columns=column_mapping)


def _process_and_calculate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    データの加工と計算を行う関数

    Args:
        df (pd.DataFrame): 元のデータフレーム

    Returns:
        pd.DataFrame: 加工と計算が行われたデータフレーム
    """

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

    return df


def _replace_nan_with_zero(df: pd.DataFrame) -> pd.DataFrame:
    """
    整数型カラムの NaN を 0 に置き換える関数

    Args:
        df (pd.DataFrame): 元のデータフレーム

    Returns:
        pd.DataFrame: NaN が 0 に置き換えられたデータフレーム
    """
    # 整数型のカラムリスト
    int_columns = [
        "G",
        "PA",
        "AB",
        "H",
        "XBH",
        "TB",
        "2B",
        "3B",
        "HR",
        "R",
        "RBI",
        "BB",
        "IBB",
        "HBP",
        "SO",
        "SB",
        "CS",
        "SAC",
        "SF",
        "GIDP",
    ]
    # すべての整数型カラムに対して NaN を 0 に置き換え
    df[int_columns] = df[int_columns].fillna(0).astype(int)
    return df
