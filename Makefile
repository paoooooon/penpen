# Makefile for penpen CLI tool

.PHONY: help build install clean test

help:
	@echo "Available targets:"
	@echo "  make build      - Build Go penpen binary"
	@echo "  make install    - Install penpen package (Python)"
	@echo "  make clean      - Remove cache files and build artifacts"
	@echo "  make test       - Run Go tests"

build:
	@echo "Building penpen binary..."
	cd go && go build -o penpen ./cmd/penpen
	@echo "Build complete: go/penpen"

test:
	@echo "Running Go tests..."
	cd go && go test ./...

install:
	@echo "Installing penpen..."
	pip install -e .
	@echo "Install complete. Run 'penpen --help' for usage."

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f go/penpen
	@echo "Cleaned up"