# Guia Completo para Rodar o Projeto com Docker

Este guia foi escrito para uma pessoa leiga conseguir baixar, instalar, iniciar, usar, desligar e remover o ambiente deste projeto do inicio ao fim.

O fluxo descrito aqui parte do repositório oficial publicado no GitHub:

- `https://github.com/victorhss21/opencode-workspace-for-data-science`

Esse repositório concentra o ambiente Docker com OpenCode e o projeto de Ciencia de Dados montado dentro do workspace.

## O que voce vai instalar

Voce vai usar 3 coisas principais:

- `Git`: para baixar o projeto do GitHub
- `Docker Desktop`: para rodar o sistema sem configurar tudo manualmente no computador
- navegador web: para abrir a interface do OpenCode

Dentro do container, o ambiente ja foi preparado para incluir:

- `Python 3.11`
- `uv`
- `OpenCode`
- bibliotecas de Ciencia de Dados
- suporte a `MLflow`

## Visao geral do que vai acontecer

Voce vai seguir esta ordem:

1. Instalar Git e Docker Desktop
2. Baixar o repositorio do GitHub
3. Configurar o arquivo `.env`
4. Subir o ambiente com Docker
5. Abrir o OpenCode no navegador
6. Inicializar o projeto de Ciencia de Dados
7. Treinar o modelo, abrir o MLflow e gerar predicoes
8. Desligar o ambiente quando terminar
9. Desinstalar tudo, se quiser remover o sistema do computador

## 1. Instalar os programas necessarios

### Git

Instale o Git pelo site oficial:

- `https://git-scm.com/downloads`

Depois da instalacao, abra um terminal e teste:

```bash
git --version
```

Se aparecer a versao do Git, esta certo.

### Docker Desktop

Instale o Docker Desktop pelo site oficial:

- `https://www.docker.com/products/docker-desktop/`

Depois de instalar:

- abra o Docker Desktop
- espere ele terminar de iniciar
- confirme que ele esta rodando

No terminal, teste:

```bash
docker --version
docker compose version
```

Se os dois comandos responderem com uma versao, esta pronto.

## 2. Baixar o repositorio do GitHub

Escolha uma pasta do seu computador onde voce quer guardar o projeto.

Exemplo:

```bash
mkdir -p ~/opencode
cd ~/opencode
git clone https://github.com/victorhss21/opencode-workspace-for-data-science
cd opencode-workspace-for-data-science
```

Ao entrar na pasta do projeto, voce devera ver arquivos como:

- `docker-compose.yml`
- `docker-configs/Dockerfile`
- `.env.example`
- `projects/meu_projeto_ds/`

## 3. Configurar o arquivo `.env`

O arquivo `.env` guarda senhas e chaves locais do seu ambiente.

Crie esse arquivo copiando o modelo de exemplo:

```bash
cp .env.example .env
```

Depois, abra o arquivo `.env` e preencha os valores.

Exemplo de campos esperados:

```env
OPENAI_API_KEY=coloque-sua-chave-aqui
ANTHROPIC_API_KEY=coloque-sua-chave-aqui
GROQ_API_KEY=coloque-sua-chave-aqui
OPENCODE_SERVER_USERNAME=opencode
OPENCODE_SERVER_PASSWORD=crie-uma-senha-forte
PYTHONUNBUFFERED=1
```

Importante:

- se voce for usar login por navegador com OpenAI, a chave `OPENAI_API_KEY` pode nao ser o caminho principal de uso, mas ainda assim o `.env` deve existir
- nunca compartilhe esse arquivo
- nunca envie esse arquivo para o GitHub

## 4. Subir o sistema com Docker

Ainda na raiz do projeto, rode:

```bash
docker compose up -d --build
```

O que esse comando faz:

- monta a imagem Docker
- cria o container do OpenCode
- expoe a interface web na sua maquina
- monta o projeto dentro do container

Na primeira execucao, pode demorar alguns minutos.

Para acompanhar o andamento, rode:

```bash
docker compose logs -f
```

Quando tudo estiver funcionando, a interface deve ficar disponivel em:

- `http://localhost:4096`

## 5. Acessar o sistema no navegador

Abra no navegador:

- `http://localhost:4096`

Se a tela pedir login, use os dados definidos no seu `.env`:

- usuario: valor de `OPENCODE_SERVER_USERNAME`
- senha: valor de `OPENCODE_SERVER_PASSWORD`

Se voce quiser conectar sua conta OpenAI pelo navegador, o fluxo documentado pelo workspace usa a porta de callback:

- `http://localhost:1455/auth/callback`

## 6. Entender o que esta rodando

O container foi preparado para abrir o OpenCode Web.

O projeto de Ciencia de Dados fica montado dentro do container e pode ser acessado para desenvolvimento e execucao.

No projeto atual, os comandos principais sao:

- `make install`: instala dependencias com `uv`
- `make train`: executa o treino do modelo
- `make mlflow-ui`: abre a interface do MLflow
- `make predict`: executa uma predicao simples

Esses comandos existem em `Makefile`.

## 7. Inicializar este projeto de Ciencia de Dados

Abra um terminal e entre no container:

```bash
docker compose exec opencode bash
```

No repositório publicado, a pasta do projeto no seu computador e `projects/meu_projeto_ds`, mas dentro do container ela fica montada como diretório de trabalho em `/workspace`.

Se quiser confirmar, rode:

```bash
pwd
ls
```

Se voce ja estiver na pasta do projeto, rode:

```bash
make install
```

Esse comando executa `uv sync` e instala as dependencias do projeto.

## 8. Rodar o projeto pela primeira vez

### Treinar o modelo

Dentro do container e na pasta do projeto, rode:

```bash
make train
```

O treino atual deste projeto:

- gera um conjunto pequeno de dados sinteticos
- treina um modelo simples
- registra metricas no MLflow
- salva artefatos locais

Ao final, os principais arquivos gerados ficam em:

- `mlruns/`
- `models/reports/latest-training-report.json`
- `models/serialized/meu-projeto-ds-model.pkl`
- `models/registry/latest-run.json`

## 9. Abrir o MLflow para acompanhar o treino

Depois do treino, rode:

```bash
make mlflow-ui
```

Esse comando abre a interface local do MLflow usando o diretório `mlruns/` como fallback local.

Normalmente, a interface do MLflow fica em uma porta local mostrada no terminal quando o comando inicia.

Se voce quiser parar essa tela depois, pressione:

```text
Ctrl + C
```

## 10. Gerar uma predicao simples

Depois de treinar, rode:

```bash
make predict
```

Esse comando:

- carrega o arquivo `models/serialized/meu-projeto-ds-model.pkl`
- executa uma predicao de exemplo
- mostra o resultado no terminal

Se o modelo ainda nao tiver sido treinado, a resposta esperada sera algo como `model-not-available`.

## 11. Como interagir com o sistema no dia a dia

Voce pode usar o sistema de 2 formas.

### Pela Web UI do OpenCode

Abra:

- `http://localhost:4096`

Exemplos de pedidos que voce pode fazer:

- "Explique a estrutura deste projeto"
- "Rode os testes"
- "Mostre onde o modelo e treinado"
- "Crie uma nova pipeline de inferencia"

### Pelo terminal dentro do container

Use:

```bash
docker compose exec opencode bash
```

E entao rode comandos como:

```bash
make install
make train
make predict
make test
```

## 12. Como verificar se esta tudo funcionando

Na raiz do workspace Docker, voce pode usar:

```bash
docker compose ps
docker compose logs --tail 50
```

Dentro do projeto, voce pode usar:

```bash
make test
```

Sinais de que esta tudo certo:

- `docker compose ps` mostra o container em execucao
- `http://localhost:4096` abre no navegador
- `make train` termina com sucesso
- `make predict` retorna predicoes
- o diretorio `mlruns/` passa a existir ou ganha novos registros

## 13. Como desligar o sistema

Se voce apenas quiser parar o container, rode na raiz do workspace:

```bash
docker compose down
```

Isso:

- para o container
- remove o container
- mantem volumes e dados persistidos

Se voce usou `make mlflow-ui` em um terminal separado, finalize antes com `Ctrl + C`.

## 14. Como reiniciar depois

Quando quiser voltar a usar, entre na pasta do projeto e rode:

```bash
docker compose up -d
```

Depois abra novamente:

- `http://localhost:4096`

## 15. Como desinstalar e apagar tudo

Se voce quiser remover completamente o ambiente Docker deste projeto, siga esta ordem.

### Passo 1: parar e remover o container

```bash
docker compose down -v
```

Esse comando tambem remove os volumes persistentes do Docker.

### Passo 2: remover a imagem criada

Liste as imagens:

```bash
docker images
```

Depois remova a imagem do workspace, se quiser:

```bash
docker rmi opencode-sandbox:latest
```

### Passo 3: apagar a pasta clonada do computador

Saia da pasta e remova o diretorio baixado:

```bash
cd ..
rm -rf opencode-workspace-for-data-science
```

### O que sera perdido ao desinstalar

Ao remover volumes e pasta local, voce pode perder:

- historico/configuracao local do OpenCode
- cache do `uv`
- arquivos locais em `mlruns/`
- artefatos em `models/serialized/`
- relatorios em `models/reports/`
- manifests em `models/registry/`

Se quiser guardar resultados, faca backup antes.

## 16. Problemas comuns

### O navegador nao abre `http://localhost:4096`

Tente:

```bash
docker compose ps
docker compose logs --tail 100
```

Verifique tambem se o Docker Desktop esta aberto.

### O comando `docker compose` nao existe

Isso normalmente significa que o Docker Desktop nao foi instalado corretamente ou nao terminou de iniciar.

### O comando `make train` falha

Tente primeiro:

```bash
make install
```

Depois rode de novo:

```bash
make train
```

### O comando `make predict` retorna `model-not-available`

Isso significa que o modelo ainda nao foi treinado. Rode antes:

```bash
make train
```

### O arquivo `.env` nao foi criado

Crie com:

```bash
cp .env.example .env
```

## 17. Resumo rapido

Se voce quiser apenas o caminho minimo, use:

```bash
mkdir -p ~/opencode
cd ~/opencode
git clone https://github.com/victorhss21/opencode-workspace-for-data-science
cd opencode-workspace-for-data-science
cp .env.example .env
# edite o .env
docker compose up -d --build
docker compose exec opencode bash
make install
make train
make predict
```

Depois abra:

- `http://localhost:4096`

## 18. O que este projeto faz hoje

No estado atual da base:

- o ambiente principal e Dockerizado
- o OpenCode roda em interface web
- o projeto usa `uv` como gerenciador de dependencias
- o treino usa `MLflow` em modo local-safe
- a inferencia atual e simples e local
- o projeto foi preparado para evoluir em pipelines, monitoramento e registry

Se voce quiser, o proximo passo natural e complementar este guia com um `readme_3.md` focado apenas em operacao do projeto por terminal, sem a camada Docker.
