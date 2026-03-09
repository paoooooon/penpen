# Makefile for generating OpenAPI Python client (Async + Pydantic V2)

.PHONY: help generate-client clean format

# API settings
API_URL ?= http://172.17.0.1:10000
OPENAPI_FILE ?= openapi.json
CLIENT_DIR ?= generated_client

help:
	@echo "Available targets:"
	@echo "  make download-spec       - Download OpenAPI spec from API"
	@echo "  make generate-client     - Generate async Python client (Pydantic V2)"
	@echo "  make clean               - Remove generated files"
	@echo "  make format              - Format generated Python code"

download-spec:
	@echo "Downloading OpenAPI spec from $(API_URL)..."
	curl -s $(API_URL)/openapi.json -o $(OPENAPI_FILE)
	@echo "Downloaded to $(OPENAPI_FILE)"

generate-client:
	@echo "Generating async Python client (Pydantic V2) from $(OPENAPI_FILE)..."
	docker run --rm -v "$(PWD):/local" \
		tiangolo/openapi-python-client \
		generate --url file:///local/$(OPENAPI_FILE) --output /local/$(CLIENT_DIR) --async
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