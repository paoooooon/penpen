# penpen

Claude Code を使用したタスク管理・実行ツール

## インストール

### インストールサーバーを使用

```bash
# インストール実行（Dockerコンテナ内）
curl -sSL http://host.docker.internal:10000/install.sh | INSTALL_SERVER=http://host.docker.internal:10000 bash
or
curl -sSL http://172.17.0.1:10000/install.sh | INSTALL_SERVER=http://172.17.0.1:10000 bash       
                  
# 別サーバーから実行する場合
curl -sSL http://your-server:10000/install.sh | INSTALL_SERVER=http://your-server:10000 bash
```

### インストール先

| パス | 内容 |
|-----|------|
| `~/.local/share/penpen/` | ソースコード、仮想環境 |
| `~/.local/bin/penpen` | 実行可能ファイル |

### カスタムインストール先

```bash
# インストール先を指定
curl -sSL http://host.docker.internal:10000/install.sh | INSTALL_SERVER=http://host.docker.internal:10000 INSTALL_BASE=/opt/penpen bash
```

### PATH設定

インストール後、シェルの設定ファイルに追加：

```bash
# ~/.bashrc または ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### ローカル開発用インストール

```bash
./install.sh
```

### インストールサーバーの再起動

```bash
# Docker Composeを使用する場合
docker-compose up -d install-server

# または簡易サーバーを使用する場合
pkill -f "python.* install" || true
python -m http.server 10000 &
```

## 使い方

```bash
# ヘルプ表示
penpen --help

# データベース初期化（初回のみ）
penpen db-init

# TODO作成
penpen todo -m "バックエンドAPIの実装"

# タスク分解（サブタスク作成）
penpen task -m "フロントエンドの実装"

# サブタスク実行
penpen run

# コミット
penpen commit
```

## コマンド一覧

| コマンド | 説明 |
|---------|------|
| `penpen todo -m "内容"` | TODOを作成しtodosテーブルに保存 |
| `penpen task -m "内容"` | タスクを分解しtodo_subtasksテーブルに保存 |
| `penpen run` | todo_subtasksから優先度の高いタスクを実行 |
| `penpen commit` | Claude Codeでコミットを実行 |
| `penpen db-init` | スキーマからデータベースを初期化 |

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `DB_PATH` | データベースファイルのパス | `~/penpen.db` |
| `API_BASE_URL` | APIのベースURL | `http://172.17.0.1:10000` |
| `INSTALL_BASE` | インストール先ベースディレクトリ | `~/.local` |

## モジュール構成

```
src/penpen/
├── cli.py        # CLIエントリーポイント
├── executor.py   # 実行レイヤー（Claude Code実行）
├── prompts.py    # プロンプト生成レイヤー
└── __main__.py   # python -m penpen 用エントリ
```

## データベース構成

### テーブル一覧

| テーブル | 説明 |
|---------|------|
| `questions` | 質問管理 |
| `todos` | タスク管理 |
| `todo_subtasks` | サブタスク管理 |

### todos ステータス

| 値 | 説明 |
|----|------|
| `todo` | 未着手 |
| `in_progress` | 進行中 |
| `completed` | 完了 |
| `cancelled` | キャンセル |

## 開発

### セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### テスト実行

```bash
python -m penpen --help
```