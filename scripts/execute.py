from datetime import datetime
import os
from create_batting_stats import create_batting_stats_db


def _create_output_directory() -> str:
    """
    出力ディレクトリを作成し、パスを返す
    """
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir_path = f"output/{now_str}"
    os.makedirs(output_dir_path, exist_ok=True)
    return output_dir_path


def main():
    output_dir_path = _create_output_directory()

    # 打撃成績のDBを作成
    create_batting_stats_db(output_dir_path)


if __name__ == "__main__":
    main()
