# 440-data
.440 用のデータを用意するためのリポジトリ

## 環境構築

### IDE

VS Code での開発を想定しています。
また、以下拡張機能のインストールを想定しています。

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

### 仮想環境

> パッケージを実行環境にインストールする際には、パッケージ等の組み合わせ等によりプログラムが動かなくなることを避けるため、プロジェクトの用途に応じて仮想環境を作成し、仮想環境に必要なパッケージをインストールし開発を行うことが望ましいらしい。

ようです。
なので、仮想環境を作成します。

参考
https://qiita.com/starfieldKt/items/ed7dee5142d9d5c177fd

#### 仮想環境の作成と設定

```zsh
# `venv` という名前の仮想環境をプロジェクト内に作成
python3 -m venv .venv
```

作成後、VS Code でコマンドパレットを開き、`Python: Select Interpreter` で作成した仮想環境を選択する。
※「('.venv': venv)」と記載のあるものを選択する。

参考
https://zenn.dev/sion_pn/articles/d0f9e45716cabb#%E4%BD%9C%E6%A5%AD%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%81%B8%E7%A7%BB%E5%8B%95

パッケージ等は、上記で作成した仮想環境内でインストールする。
インストールする際、.venv をアクティブにする。

```zsh
# 仮想環境をアクティブに
# アクティブになると、ターミナルの先頭に (.venv) が表示されるする
source .venv/bin/activate

# 仮想環境を非アクティブにする
deactivate
```