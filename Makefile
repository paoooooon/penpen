# Makefile for penpen CLI tool

.PHONY: help install clean

help:
	@echo "Available targets:"
	@echo "  make install    - Install penpen package"
	@echo "  make clean      - Remove cache files"

install:
	@echo "Installing penpen..."
	pip install -e .
	@echo "Install complete. Run 'penpen --help' for usage."

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned up"