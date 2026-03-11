// Package executor provides Claude Code execution functionality
package executor

import (
	"fmt"
	"os"
	"os/exec"
)

// RunClaudeCommand executes a Claude Code command with the given message
func RunClaudeCommand(message string) int {
	// Set environment variables
	env := os.Environ()
	env = append(env, "ANTHROPIC_AUTH_TOKEN=ollama")
	env = append(env, "ANTHROPIC_API_KEY=")
	env = append(env, "ANTHROPIC_BASE_URL=http://localhost:11434")
	env = append(env, "OLLAMA_CONTEXT_LENGTH=65536")

	cmd := exec.Command("claude",
		"--model", "glm-5:cloud",
		"--output-format", "stream-json",
		"--verbose",
		"--include-partial-messages",
		"--allowedTools", "Read,Edit,Bash",
		"-p", message,
	)
	cmd.Env = env
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	fmt.Println("=== Claude Code 実行 ===")
	fmt.Printf("メッセージ: %s\n\n", message)

	if err := cmd.Run(); err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			fmt.Printf("\n終了コード: %d\n", exitErr.ExitCode())
			return exitErr.ExitCode()
		}
		fmt.Printf("\nエラー: %v\n", err)
		return 1
	}

	fmt.Println("\n終了コード: 0")
	return 0
}
