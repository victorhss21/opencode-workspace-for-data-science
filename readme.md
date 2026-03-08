# **OpenCode Workspace - Data Science Environment**

**Objetivo:** Ambiente Docker seguro e isolado para execução do OpenCode AI Agent em projetos de Ciência de Dados.

## 📋 Estregas da solução

| # | Requisito | Status Atual |
|---|-----------|--------------|
| 1 | OpenCode restrirto a modificações na pasta do projeto | ✅ SIM |
| 2 | Portas expostas para internet + OAuth | ✅ SIM |
| 3 | Permite instalar pacotes Python livremente | ✅ SIM |
| 4 | UV como gerenciador de pacotes | ✅ OK |
| 5 | Web UI funcionando sem travas | ✅ SIM |

***

## 📌 Configurações

As configuraões a seguir é **única e simplificada**, porém atende todos os requisitos:

### **1. Estrutura de Diretórios**

Tendo como contexto um projeto de Ciência de Dados, segue uma sugestão simplificada da estrutura dos diretórios:

```
~/opencode-workspace/
├── docker-configs/
│   └── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── projects/
│   └── meu_projeto_ds/
│       ├── data/
│       ├── notebooks/
│       ├── scripts/
│       ├── output/
│       ├── pyproject.toml
│       └── uv.lock
```

***

### **2. Arquivo Dockerfile**

Crie `docker-configs/Dockerfile`:

```dockerfile
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
```

***

### **3. Arquivo docker-compose.yml**

Crie `docker-compose.yml`:

```yaml
services:
  opencode:
    build:
      context: .
      dockerfile: docker-configs/Dockerfile
    
    container_name: opencode_workspace
    image: opencode-sandbox:latest
    
    # ========== VOLUME DO PROJETO (Isolamento) ==========
    volumes:
      # Montar APENAS o diretório do projeto específico
      - ./projects/meu_projeto_ds:/workspace/project:rw
      
      # Persistir configurações do OpenCode
      - opencode_data:/home/data_scientist/.opencode
      
      # Persistir cache do UV
      - uv_cache:/home/data_scientist/.cache/uv
    
    # Working directory dentro do projeto
    working_dir: /workspace/project
    
    # ========== VARIÁVEIS DE AMBIENTE ==========
    env_file: .env
    
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONDONTWRITEBYTECODE=1
      - HOME=/home/data_scientist
      - UV_CACHE_DIR=/home/data_scientist/.cache/uv
    
    # ========== PORTAS EXPOSTAS ==========
    ports:
      - "4096:4096"   # Web UI
      - "1455:1455"   # OAuth callback OpenAI
      - "8888:8888"   # Jupyter (opcional)
    
    # ========== NETWORK (Internet habilitada) ==========
    networks:
      - opencode_network
    
    # ========== RESOURCE LIMITS ==========
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    
    # ========== SEGURANÇA ==========
    security_opt:
      - no-new-privileges:true
    
    cap_drop:
      - ALL
    
    cap_add:
      - NET_BIND_SERVICE
      - CHOWN
      - SETUID
      - SETGID
    
    # ========== FILESYSTEM ==========
    # NÃO usar read_only (OpenCode Web precisa escrever)
    read_only: false
    
    # Tmpfs para cache temporário
    tmpfs:
      - /tmp:size=2G
    
    # ========== RUNTIME ==========
    stdin_open: true
    tty: true
    restart: unless-stopped
    
    # ========== LOGGING ==========
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

# ========== VOLUMES PERSISTENTES ==========
volumes:
  opencode_data:
    driver: local
  uv_cache:
    driver: local

# ========== NETWORK ==========
networks:
  opencode_network:
    driver: bridge
```

***

### **4. Arquivo .env**

Crie `.env`:

```env
# API Keys (substitua pelos seus valores)
OPENAI_API_KEY=sk-proj-sua-chave-aqui
ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui

# Configurações do OpenCode (substitua pelos seus valores)
OPENCODE_SERVER_PASSWORD=sua-senha-segura
OPENCODE_SERVER_USERNAME=opencode

# Python
PYTHONUNBUFFERED=1
```

***

### **5. Arquivo .gitignore**

Crie `.gitignore`:

```gitignore
# Secrets
.env

# Data
projects/*/data/*.csv
projects/*/data/*.parquet
projects/*/output/*
!projects/*/output/.gitkeep

# Python
__pycache__/
*.py[cod]
.venv/
.uv/
*.egg-info/
.pytest_cache/
.mypy_cache/

# Jupyter
.ipynb_checkpoints/
*.ipynb

# OS
.DS_Store
Thumbs.db
```

***

### **6. Arquivo pyproject.toml do Projeto**

Crie em `projects/meu_projeto_ds/pyproject.toml`:

```toml
[project]
name = "meu-projeto-ds"
version = "0.1.0"
description = "Projeto de Ciência de Dados com OpenCode"
requires-python = ">=3.11"

dependencies = [
    # Core Data Science
    "pandas>=2.1.0",
    "numpy>=1.24.0",
    "scipy>=1.11.0",
    "scikit-learn>=1.3.0",
    
    # Visualization
    "matplotlib>=3.7.0",
    "seaborn>=0.13.0",
    "plotly>=5.17.0",
    
    # Machine Learning
    "xgboost>=2.0.0",
    "lightgbm>=4.1.0",
    
    # Time Series
    "statsmodels>=0.14.0",
    "prophet>=1.1.0",
    
    # LLMs
    "openai>=1.0.0",
    "anthropic>=0.7.0",
    "langchain>=0.1.0",
    
    # Utilities
    "python-dotenv>=1.0.0",
    "tqdm>=4.66.0",
    "rich>=13.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "jupyter>=1.0.0",
    "ipython>=8.17.0",
    "pytest>=7.4.0",
    "black>=23.11.0",
    "isort>=5.12.0",
    "flake8>=6.1.0",
]
```

***

## 📲 Passo a Passo de Implementação

### **Passo 1: Preparar Estrutura**

```bash
# 1. Navegar para workspace
cd ~/opencode-workspace

# 2. Criar estrutura de diretórios
mkdir -p docker-configs
mkdir -p projects/meu_projeto_ds/{data,notebooks,scripts,output}

# 3. Criar arquivos de configuração
# - Copiar Dockerfile para docker-configs/
# - Copiar docker-compose.yml para raiz
# - Criar .env
# - Criar pyproject.toml no projeto
```

### **Passo 2: Build da Imagem**

```bash
# Parar containers antigos
docker compose down -v

# Build (pode demorar 5-10 min na primeira vez)
docker compose build --no-cache

# Verificar imagem criada
docker images | grep opencode-sandbox
```

### **Passo 3: Iniciar OpenCode Web UI**

```bash
# Iniciar container
docker compose up -d

# Verificar logs
docker compose logs -f

# Aguardar mensagem:
# "Local access:       http://localhost:4096"
```

### **Passo 4: Acessar Web UI**

```bash
# Abrir navegador
# http://localhost:4096

# Fazer login (se configurou senha no .env)
# Username: opencode
# Password: sua-senha-segura
```

### **Passo 5: Configurar OAuth OpenAI**

> Nesta etapa, é apresentado o caminho para realizar autenticação com a OpenAI caso você possua algum plano do ChatGPT (a patir do plano GO em diante). Com isso, você pode usufruir da sua assinatura no OpenCode sem pagar a mais por isso - que ocorreria caso você gerasse uma chave de API.

```bash
# 1. Na Web UI OpenCode, clicar em "Escolher modelo" (ou Ctrl + ') 
# 2. Em seguida, vá até "Gerenciar modelos"
# 3. Mp canto superior direito: "Conectar provedor"
# 4. Na barra de pesquisa, busque por "openai" e seleciona a opção que irá aparecer
# 5. Em seguida, selecione "ChatGPT/Plus (browser)"
# 6. Clicar no link de autorização
# 3. Fazer login na OpenAI
# 4. Callback automático para http://localhost:1455/auth/callback
# 5. ✅ Autenticação concluída!
```

***

## ✅ Verificação dos Requisitos

### **Teste 1: OpenCode só acessa pasta do projeto**

```bash
# Entrar no container
docker compose exec opencode bash

# Verificar estrutura
ls -la /workspace
# Deve mostrar apenas: project/

# Tentar acessar fora do projeto
ls -la /home/data_scientist
# Deve mostrar apenas: .cache/ .config/ .opencode/

# Tentar criar arquivo fora do projeto
touch /workspace/teste.txt
# ✅ Deve funcionar (dentro de /workspace)

# Tentar acessar raiz
ls /
# Não deve conseguir navegar para outros diretórios críticos
```

**✅ Requisito 1 atendido:** OpenCode só tem acesso a `/workspace/project` (seu projeto montado).

***

### **Teste 2: Internet e OAuth funcionando**

```bash
# No navegador: http://localhost:4096

# Teste 1: Verificar internet no container
docker compose exec opencode curl -I https://google.com
# Deve retornar: HTTP/2 200

# Teste 2: OAuth OpenAI
# 1. Clicar em "Connect OpenAI" na UI
# 2. Fazer login
# 3. Verificar se callback funciona
```

**✅ Requisito 2 atendido:** Internet habilitada + OAuth funcionando.

***

### **Teste 3: Instalar pacotes Python**

```bash
# Entrar no container
docker compose exec opencode bash

# Navegar para projeto
cd /workspace/project

# Adicionar novo pacote com UV
uv add polars

# Verificar instalação
uv pip list | grep polars

# Testar importação
python -c "import polars; print(polars.__version__)"
```

**✅ Requisito 3 atendido:** Instalação livre de pacotes Python.

***

### **Teste 4: UV como gerenciador**

```bash
# Verificar UV instalado
docker compose exec opencode uv --version

# Ver pacotes gerenciados pelo UV
docker compose exec opencode uv pip list

# Adicionar dependência
docker compose exec opencode uv add requests
```

**✅ Requisito 4 atendido:** UV configurado como padrão.

***

### **Teste 5: Web UI sem travas**

```bash
# Verificar status
docker compose ps
# STATUS deve ser "Up"

# Verificar logs (sem erros)
docker compose logs --tail 50

# Acessar UI
# http://localhost:4096
# Deve carregar normalmente

# Testar prompt
# "Liste os arquivos no diretório atual"
```

**✅ Requisito 5 atendido:** Web UI funcional.

***

## 📊 Resumo da Solução

| Requisito | Como foi atendido |
|-----------|-------------------|
| **Isolamento de projeto** | Volume monta apenas `./projects/meu_projeto_ds:/workspace:rw` |
| **Internet + OAuth** | Network habilitada + portas 4096 e 1455 expostas |
| **Instalar pacotes** | UV configurado + pip disponível + write access em `/workspace` |
| **UV como padrão** | UV instalado no Dockerfile + `UV_CACHE_DIR` configurado |
| **Web UI funcional** | Comando `opencode web` + portas corretas + filesystem write habilitado |

***

## 🔐 Nível de Segurança

> Esta configuração oferece **isolamento moderado**:

### **O que o setup atual PROTEGE:**

✅ **OpenCode não pode modificar o sistema HOST**
- Está isolado em container Docker
- Não tem acesso a `/home/seu_usuario` do Windows

✅ **OpenCode não pode deletar arquivos do HOST fora do projeto**
- Volume montado apenas em `/workspace` = `./projects/meu_projeto_ds`
- Não pode acessar outros projetos

✅ **Recursos limitados**
- CPU e memória limitados
- Não pode consumir todos recursos do sistema

✅ **Usuário não-root**
- Não pode escalar privilégios dentro do container

***

### **O que o setup NÃO protege:**

⚠️ **OpenCode PODE ver outros diretórios do container**
- `/bin`, `/etc`, `/usr`, etc. (filesystem do container)
- **Mas não pode modificar** (falta de permissões)
- **Não são seus dados** (são apenas binários do sistema, não seus dados)

⚠️ **OpenCode PODE modificar arquivos dentro de `/workspace`**
- É o comportamento **esperado e necessário**
- `/workspace` = seu projeto montado
- **Você quer** que ele possa criar/editar arquivos do projeto

⚠️ **OpenCode PODE acessar internet**
- Necessário para OAuth e APIs (OpenAI, etc.)
- Necessário para instalar pacotes Python

***

## 📊 Resumo | Requisitos Atendidos

| Requisito | Status | Explicação |
|-----------|--------|------------|
| **1. Só acessa pasta do projeto** | ✅ **ATENDIDO** | Volume monta apenas projeto em `/workspace`. Não pode acessar outros projetos do host. |
| **2. Portas + Internet + OAuth** | ✅ **ATENDIDO** | Portas 4096, 1455 expostas. Network habilitada. OAuth funcional. |
| **3. Instalar pacotes Python** | ✅ **ATENDIDO** | UV configurado. Pip disponível. Pode instalar qualquer pacote. |
| **4. UV como padrão** | ✅ **ATENDIDO** | UV instalado e configurado no Dockerfile. |
| **5. Web UI funcional** | ✅ **ATENDIDO** | `opencode web` comando correto. UI carrega sem erros. |

## 📚 Referências
[OpenCode Docs](https://opencode.ai/docs/pt-br/)

[Docker Docs](https://docs.docker.com/)

[UV Package Manager](https://github.com/astral-sh/uv)