// Package database provides SQLite database operations
package database

import (
	"database/sql"
	"fmt"

	_ "modernc.org/sqlite"

	"penpen/internal/schema"
)

// DB represents a database connection
type DB struct {
	*sql.DB
}

// Open opens a database connection
func Open(dsn string) (*DB, error) {
	db, err := sql.Open("sqlite", dsn)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}
	return &DB{db}, nil
}

// InitSchema initializes the database schema
func (db *DB) InitSchema() error {
	_, err := db.Exec(schema.SchemaSQL)
	if err != nil {
		return fmt.Errorf("failed to initialize schema: %w", err)
	}
	return nil
}

// GetIncompleteSubtasksCount returns the count of incomplete todo_subtasks
func (db *DB) GetIncompleteSubtasksCount() (int, error) {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM todo_subtasks WHERE status != 'completed'").Scan(&count)
	if err != nil {
		return 0, fmt.Errorf("failed to get incomplete subtasks count: %w", err)
	}
	return count, nil
}
