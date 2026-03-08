FROM node:20-slim

# ========== INSTALAÇÃO DE DEPENDÊNCIAS DO SISTEMA ==========
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-distutils \
    python3.11-venv \
    python3-pip \
    build-essential \
    git \
    curl \
    wget \
    ca-certificates \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ========== CONFIGURAR PYTHON ==========
RUN ln -sf /usr/bin/python3.11 /usr/bin/python

# ========== INSTALAR UV (Gerenciador de Pacotes) ==========
RUN pip install --no-cache-dir --break-system-packages uv

# ========== INSTALAR PACOTES BASE DE DATA SCIENCE ==========
RUN pip install --no-cache-dir --break-system-packages \
    pandas numpy scipy scikit-learn \
    matplotlib seaborn plotly \
    jupyter jupyterlab ipython ipywidgets \
    openai anthropic groq langchain \
    python-dotenv pydantic pydantic-settings \
    pytest black isort flake8 mypy \
    sqlalchemy psycopg2-binary \
    requests tqdm rich loguru \
    mlflow wandb statsmodels prophet

# ========== INSTALAR OPENCODE ==========
RUN npm install -g opencode-ai@latest

# ========== CRIAR USUÁRIO NÃO-ROOT ==========
RUN useradd -m -u 9000 -s /bin/bash data_scientist

# ========== CONFIGURAR DIRETÓRIOS ==========
RUN mkdir -p /workspace && \
    mkdir -p /home/data_scientist/.cache && \
    mkdir -p /home/data_scientist/.config && \
    chown -R data_scientist:data_scientist /workspace && \
    chown -R data_scientist:data_scientist /home/data_scientist

# ========== CONFIGURAÇÕES FINAIS ==========
USER data_scientist
WORKDIR /workspace

ENV PATH="/home/data_scientist/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD opencode --version || exit 1

CMD ["opencode", "web", "--hostname", "0.0.0.0", "--port", "4096"]
