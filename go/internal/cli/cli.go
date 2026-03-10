// Package cli provides command-line interface functionality
package cli

import (
	"fmt"
	"os"

	"penpen/internal/database"
	"penpen/internal/env"
	"penpen/internal/executor"
	"penpen/internal/prompts"
)

// Command represents a CLI command
type Command struct {
	Name        string
	Description string
	Execute     func(args []string) int
}

// Commands returns available CLI commands
func Commands() map[string]Command {
	return map[string]Command{
		"commit": {
			Name:        "commit",
			Description: "Claude Codeでコミットを実行",
			Execute: func(args []string) int {
				prompt := prompts.Commit()
				return executor.RunClaudeCommand(prompt)
			},
		},
		"init-db": {
			Name:        "init-db",
			Description: "スキーマからデータベースを初期化",
			Execute: func(args []string) int {
				dbPath := env.DBPath()
				db, err := database.Open(dbPath)
				if err != nil {
					fmt.Fprintf(os.Stderr, "データベースエラー: %v\n", err)
					return 1
				}
				defer db.Close()

				if err := db.InitSchema(); err != nil {
					fmt.Fprintf(os.Stderr, "スキーマ初期化エラー: %v\n", err)
					return 1
				}

				fmt.Printf("データベースを初期化しました: %s\n", dbPath)
				return 0
			},
		},
		"todo": {
			Name:        "todo",
			Description: "Claude CodeでTODOを作成",
			Execute: func(args []string) int {
				if len(args) == 0 {
					fmt.Fprintln(os.Stderr, "エラー: -m/--message オプションが必要です")
					return 1
				}
				message := args[len(args)-1]
				prompt := prompts.Todo(message)
				return executor.RunClaudeCommand(prompt)
			},
		},
		"task": {
			Name:        "task",
			Description: "Claude Codeでタスクを分解してサブタスクを作成",
			Execute: func(args []string) int {
				if len(args) == 0 {
					fmt.Fprintln(os.Stderr, "エラー: -m/--message オプションが必要です")
					return 1
				}
				message := args[len(args)-1]
				prompt := prompts.Task(message)
				return executor.RunClaudeCommand(prompt)
			},
		},
		"run": {
			Name:        "run",
			Description: "サブタスクを実行",
			Execute: func(args []string) int {
				dbPath := env.DBPath()
				db, err := database.Open(dbPath)
				if err != nil {
					fmt.Fprintf(os.Stderr, "データベースエラー: %v\n", err)
					return 1
				}
				defer db.Close()

				count, err := db.GetIncompleteSubtasksCount()
				if err != nil {
					fmt.Fprintf(os.Stderr, "エラー: %v\n", err)
					return 1
				}

				if count == 0 {
					fmt.Println("実行するサブタスクがありません")
					return 0
				}

				fmt.Printf("未完了サブタスク数: %d\n", count)
				for i := 0; i < count; i++ {
					fmt.Printf("\n--- サブタスク %d/%d ---\n", i+1, count)
					prompt := prompts.Run()
					result := executor.RunClaudeCommand(prompt)

					fmt.Printf("\n--- コミット %d/%d ---\n", i+1, count)
					executor.RunClaudeCommand(prompts.Commit())

					if result != 0 {
						fmt.Printf("サブタスク実行エラー (終了コード: %d)\n", result)
						return result
					}
				}
				return 0
			},
		},
	}
}
