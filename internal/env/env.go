// Package env provides environment variable management
package env

import (
	"os"
	"path/filepath"
)

// DBPath returns the database file path from environment variable or default
func DBPath() string {
	dbPath := os.Getenv("DB_PATH")
	if dbPath == "" {
		// Default: current directory + .env.Don't_touch_the_AI.db
		cwd, err := os.Getwd()
		if err != nil {
			cwd = "."
		}
		dbPath = filepath.Join(cwd, ".env.Don't_touch_the_AI.db")
	}
	return dbPath
}
