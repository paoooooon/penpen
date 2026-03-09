FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"

# Update and install basic tools
#RUN apt-get update && apt-get install -y \
    #git \
    #curl \
    #wget \
    #vim \
    #nano \
    #jq \
    #less \
    #tree \
    #htop \
    #python3 \
    #python3-pip \
    #python3-venv \
    #nodejs \
    #npm \
    #sqlite3 \
    #zstd 


RUN apt-get update && apt-get install -y \
    curl ca-certificates \
    git wget vim nano jq less tree htop \
    python3 python3-pip python3-venv \
    sqlite3 zstd \
 && rm -rf /var/lib/apt/lists/*

# Node.js 24 (NodeSource)
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
 && apt-get update && apt-get install -y nodejs \
 && rm -rf /var/lib/apt/lists/*

# Install Claude CLI
RUN curl -fsSL https://claude.ai/install.sh | bash

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Install additional Python packages
RUN pip3 install --break-system-packages \
    anthropic \
    openai \
    rich \
    pyyaml \
    python-dotenv

# Create workspace directory
WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]