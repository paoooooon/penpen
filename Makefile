# Makefile for generating OpenAPI Python client (Async + Pydantic V2)

.PHONY: help generate-client clean format

# API settings
API_URL ?= http://172.17.0.1:10000
OPENAPI_FILE ?= openapi.yaml
CLIENT_DIR ?= generated_client

help:
	@echo "Available targets:"
	@echo "  make download-spec       - Download OpenAPI spec from API"
	@echo "  make generate-client     - Generate async Python client (Pydantic V2)"
	@echo "  make clean               - Remove generated files"
	@echo "  make format              - Format generated Python code"

download-spec:
	@echo "Downloading OpenAPI spec from $(API_URL)..."
	curl -s $(API_URL)/openapi.yaml -o $(OPENAPI_FILE)
	@echo "Downloaded to $(OPENAPI_FILE)"

generate-client:
	@echo "Generating async Python client (Pydantic V2) from $(OPENAPI_FILE)..."
	.venv/bin/openapi-python-client generate --path $(OPENAPI_FILE) --output-path $(CLIENT_DIR) --overwrite
	@echo "Client generated in $(CLIENT_DIR)/"
	@echo "Install deps: pip install httpx httpx[http2] pydantic"

clean:
	@echo "Cleaning generated files..."
	rm -rf $(CLIENT_DIR)
	rm -f $(OPENAPI_FILE)
	@echo "Cleaned up"

format:
	@echo "Formatting generated code..."
	black $(CLIENT_DIR)
	isort $(CLIENT_DIR)
	@echo "Formatted"