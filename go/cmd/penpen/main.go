// Package main is the entry point for penpen CLI
package main

import (
	"fmt"
	"os"

	"penpen/internal/cli"
)

func main() {
	commands := cli.Commands()

	if len(os.Args) < 2 {
		printHelp(commands)
		os.Exit(0)
	}

	cmdName := os.Args[1]
	cmd, ok := commands[cmdName]
	if !ok {
		fmt.Fprintf(os.Stderr, "エラー: 不明なコマンド '%s'\n\n", cmdName)
		printHelp(commands)
		os.Exit(1)
	}

	args := os.Args[2:]
	exitCode := cmd.Execute(args)
	os.Exit(exitCode)
}

func printHelp(commands map[string]cli.Command) {
	fmt.Println("penpen - Claude Code を使用したタスク管理・実行ツール")
	fmt.Println()
	fmt.Println("Usage: penpen {commit,init-db,todo,task,run} ... [-h]")
	fmt.Println()
	fmt.Println("Commands:")
	for name, cmd := range commands {
		fmt.Printf("  %-10s %s\n", name, cmd.Description)
	}
	fmt.Println()
	fmt.Println("例:")
	fmt.Println("  penpen todo -m \"バックエンドAPIの実装\"    TODOを作成")
	fmt.Println("  penpen task -m \"フロントエンドの実装\"     タスクを分解してサブタスク作成")
	fmt.Println("  penpen run                               サブタスクを実行")
	fmt.Println("  penpen commit                            コミットを実行")
	fmt.Println("  penpen init-db                           データベースを初期化")
	fmt.Println()
	fmt.Println("環境変数:")
	fmt.Println("  DB_PATH         データベースファイルのパス (デフォルト: ./.env.Don't_touch_the_AI.db)")
}
