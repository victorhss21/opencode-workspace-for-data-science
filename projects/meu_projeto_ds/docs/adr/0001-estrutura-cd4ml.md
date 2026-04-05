# ADR 0001 - Adotar estrutura CD4ML

- Status: aceito
- Data: 2026-03-13

## Contexto

O projeto precisa de uma base que favoreca experimentacao, rastreabilidade e automacao do ciclo de vida de modelos.

## Decisao

Adotar uma estrutura orientada a CD4ML, separando dados, codigo, pipelines, modelos, testes e automacoes de entrega.

## Consequencias

- melhor organizacao para times de dados e engenharia
- caminho claro para CI/CD e versionamento de artefatos
- menor acoplamento entre exploracao, treino e inferencia
