import sqlite3


def merge_databases(
    merged_db_path: str, players_db_path: str, batting_db_path: str
) -> None:
    """
    打撃成績と選手情報のDBを統合する

    :param merged_db_path: 統合後のDBファイルのパス
    :param players_db_path: 選手情報のDBファイルのパス
    :param batting_db_path: 打撃成績のDBファイルのパス
    """
    with sqlite3.connect(merged_db_path) as merged_conn:
        # 選手情報のテーブルをコピー
        _copy_tables(merged_conn, players_db_path)

        # 打撃成績のテーブルをコピー
        _copy_tables(merged_conn, batting_db_path)

    print(f"統合されたDBを作成しました: {merged_db_path}")


def _copy_tables(merged_conn: sqlite3.Connection, source_db_path: str):
    """
    ソースDBからテーブルをコピーする

    :param merged_conn: 統合先のDB接続
    :param source_db_path: ソースDBのパス
    """
    with sqlite3.connect(source_db_path) as source_conn:
        source_cursor = source_conn.cursor()
        source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = source_cursor.fetchall()

        for table in tables:
            table_name = table[0]
            source_cursor.execute(
                f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';"
            )
            create_table_sql = source_cursor.fetchone()

            if create_table_sql:
                try:
                    merged_conn.execute(create_table_sql[0])
                    source_cursor.execute(f"SELECT * FROM {table_name}")
                    rows = source_cursor.fetchall()
                    if rows:
                        columns = ", ".join(
                            f'"{col[0]}"' for col in source_cursor.description
                        )
                        placeholders = ", ".join("?" for _ in source_cursor.description)
                        merged_conn.executemany(
                            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                            rows,
                        )
                    print(f"テーブル '{table_name}' をコピーしました。")
                except sqlite3.OperationalError as e:
                    print(
                        f"テーブル '{table_name}' のコピー中にエラーが発生しました: {e}"
                    )
            else:
                print(
                    f"テーブル '{table_name}' の構造を取得できませんでした。スキップします。"
                )

    merged_conn.commit()
