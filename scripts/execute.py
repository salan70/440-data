from datetime import datetime
import os
from create_batting_stats import create_batting_stats_db
from create_players import create_players_db
from merge_database import merge_databases


def _create_output_directory() -> tuple[str, str]:
    """
    出力ディレクトリを作成し、パスを返す
    """
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_output_dir = f"output/{now_str}"
    intermediate_dir = os.path.join(main_output_dir, "intermediate")
    os.makedirs(intermediate_dir, exist_ok=True)
    return main_output_dir, intermediate_dir


def main():
    main_output_dir, intermediate_dir = _create_output_directory()

    # 選手情報のDBを作成
    players_db_path = os.path.join(intermediate_dir, "players.db")
    create_players_db(players_db_path)

    # 打撃成績のDBを作成
    batting_db_path = os.path.join(intermediate_dir, "batting_stats.db")
    create_batting_stats_db(batting_db_path)

    # DBを統合
    merge_databases(
        merged_db_path=os.path.join(main_output_dir, "baseball_stats.db"),
        players_db_path=players_db_path,
        batting_db_path=batting_db_path,
    )


if __name__ == "__main__":
    main()
