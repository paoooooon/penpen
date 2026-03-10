-- penpen database schema

-- Todos table
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'todo' CHECK(status IN ('todo', 'in_progress', 'completed', 'cancelled')),
    priority TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Todo subtasks table
CREATE TABLE IF NOT EXISTS todo_subtasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    todo_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'todo' CHECK(status IN ('todo', 'in_progress', 'completed', 'cancelled')),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_todo_subtasks_todo_id ON todo_subtasks(todo_id);
CREATE INDEX IF NOT EXISTS idx_todos_status ON todos(status);
CREATE INDEX IF NOT EXISTS idx_todo_subtasks_status ON todo_subtasks(status);

-- Table: questions
-- エージェントによる質問・疑問の管理
-- status:
--   - pending: 未解決。質問が投げかけられ、ユーザーからの回答待ちの状態
--   - provisionally_implemented: 暫定実装済み。ユーザーの確認待ちで、暫定的な解決策を実装した状態
--   - answered: 回答済み。ユーザーからの回答を受け取った状態
--   - resolved: 解決済み。質問に対する最終的な解決策が確定し、実装済みの状態
--   - cancelled: キャンセル済み。質問が無効化された、または別の方法で解決された状態
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    context TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'provisionally_implemented', 'answered', 'resolved', 'cancelled')),
    provisional_solution TEXT,
    answer TEXT,
    resolved_solution TEXT,
    todo_subtask_id INTEGER,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (todo_subtask_id) REFERENCES todo_subtasks(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_questions_status ON questions(status);
CREATE INDEX IF NOT EXISTS idx_questions_todo_subtask_id ON questions(todo_subtask_id);