
-- Programming Agent Database Schema
-- SQLite3

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Table: messages
-- 各メッセージ
-- role:
--   - user: ユーザーからのメッセージ
--   - assistant: AIアシスタントからのメッセージ
-- status:
--   - pending: 処理待ち。キューに追加され、まだ実行されていない
--   - running: 実行中。現在処理中のメッセージ
--   - completed: 完了。正常に処理が終了した状態
--   - cancelled: キャンセル済み。実行中または待機中にキャンセルされた状態
--   - error: エラー発生。処理中にエラーが発生した状態
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    metadata TEXT,
    status TEXT NOT NULL DEFAULT 'completed' CHECK(status IN ('pending', 'running', 'completed', 'cancelled', 'error')),
    queue_order INTEGER,
    completed_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Table: questions
-- 質問・疑問の管理
-- status:
--   - pending: 未解決。質問が投げかけられ、ユーザーからの回答待ちの状態
--   - provisionally_implemented: 暫定実装済み。ユーザーの確認待ちで、暫定的な解決策を実装した状態
--   - answered: 回答済み。ユーザーからの回答を受け取った状態
--   - resolved: 解決済み。質問に対する最終的な解決策が確定し、実装済みの状態
--   - cancelled: キャンセル済み。質問が無効化された、または別の方法で解決された状態
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE,
    question TEXT NOT NULL,
    context TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'provisionally_implemented', 'answered', 'resolved', 'cancelled')),
    provisional_solution TEXT,
    answer TEXT,
    resolved_solution TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Table: todos
-- タスク管理
-- status:
--   - todo: 未着手。タスクが作成され、まだ開始されていない状態
--   - in_progress: 進行中。現在作業中のタスク
--   - completed: 完了。タスクが完了した状態
--   - cancelled: キャンセル済み。タスクが取り消された状態
-- priority:
--   - low: 低優先度
--   - medium: 中優先度（デフォルト）
--   - high: 高優先度
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'todo' CHECK(status IN ('todo', 'in_progress', 'completed', 'cancelled')),
    priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high')),
    due_date TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Table: todo_subtasks
-- サブタスク管理
-- status:
--   - todo: 未完了。サブタスクがまだ完了していない状態
--   - completed: 完了。サブタスクが完了した状態
--   - cancelled: キャンセル済み。サブタスクが取り消された状態
-- sort_order: 表示順序（小さい値ほど先頭に表示）
CREATE TABLE IF NOT EXISTS todo_subtasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE,
    todo_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'todo' CHECK(status IN ('todo', 'completed', 'cancelled')),
    sort_order INTEGER NOT NULL DEFAULT 0,
    completed_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_questions_status ON questions(status);
CREATE INDEX IF NOT EXISTS idx_todos_status ON todos(status);
CREATE INDEX IF NOT EXISTS idx_todo_subtasks_todo_id ON todo_subtasks(todo_id);