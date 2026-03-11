// Package prompts provides prompt generation functions
package prompts

import (
	"fmt"

	"penpen/internal/env"
)

// Commit generates a prompt for git commit
func Commit() string {
	return "適度な粒度でコミットして　メッセージは日本語で　必要に応じて、.gitignoreを追加して"
}

// Todo generates a prompt for creating a TODO
func Todo(message string) string {
	return fmt.Sprintf(`%s
実装するにあたって、どんな作業が必要か、%sのtodosテーブルに保存してください。
これはあなた以外の人が見るので別の人が見返してわかるように客観的にお願いします
todo_subtasksの作成は不要です。 todosテーブルに詳しく書いてください`, message, env.DBPath())
}

// Task generates a prompt for breaking down a task into subtasks
func Task(message string) string {
	return fmt.Sprintf(`%s
%sのtodosテーブルを実装するにあたって、どんな作業が必要か、
%sのtodo_subtasksテーブルに保存してください。
これはあなた以外の人が見るので別の人が見返してわかるように客観的にお願いします`, message, env.DBPath(), env.DBPath())
}

// Raw generates a prompt for raw input
func Raw(message string) string {
	return message
}

// Run generates a prompt for running a subtask
func Run() string {
	return fmt.Sprintf(`%sのtodo_subtasksテーブルの中から、優先度の高いものを1つ選んで、実装してください。実装が終わったらステータスの更新をしてください
仕様でわからないところがあったら、仮説を立てて実装してください。どのような疑問で、どのような対応をしたのか、questionsテーブルに追加してください。
実装に関して、コマンドで生成すべきファイルを直接編集しないこと`, env.DBPath())
}
