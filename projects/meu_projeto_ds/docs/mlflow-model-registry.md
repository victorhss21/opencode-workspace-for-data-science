# MLflow Model Registry

Este documento explica como o projeto usa o conceito de Model Registry do MLflow para versionar modelos e preparar promocao controlada.

## O que e model registry

Model Registry e a camada do MLflow responsavel por organizar modelos versionados ao longo do tempo.

Enquanto o tracking responde "como foi esta execucao?", o registry responde:

- qual e a versao atual do modelo?
- quais versoes ja existiram?
- qual run originou cada versao?
- qual modelo e candidato a promocao?
- qual modelo esta aprovado para producao?

Esse e um ponto central de maturidade em MLOps: sair de "tenho um arquivo .pkl" para "tenho um modelo governado".

## Como esta implementado aqui

### Nome estavel do modelo

O projeto trabalha com um nome logico estavel via:

- `MLFLOW_MODEL_NAME`

Hoje o default e `meu-projeto-ds-model`.

Esse nome deve permanecer estavel. O que muda ao longo do tempo e a versao do modelo, nao o nome conceitual.

### Registro da versao

Depois que o treino loga o modelo em `src/meu_projeto_ds/models/train.py`, o projeto chama:

- `register_model_version()` em `src/meu_projeto_ds/models/tracking.py`

Essa funcao tenta:

1. garantir que o registered model exista
2. registrar uma nova versao a partir do `model_uri`
3. devolver status, numero da versao e eventual erro

Isso faz com que o retorno de `train()` inclua campos como:

- `model_name`
- `model_version`
- `registration_status`
- `registration_error`

## Tracking nao e registry

Essa separacao precisa ficar muito clara:

- tracking guarda a historia de cada execucao
- registry organiza o ciclo de vida das versoes do modelo

Uma run pode existir sem virar uma versao registrada.

Uma versao registrada, por outro lado, deve apontar para uma run rastreavel e auditavel.

## O papel de `models/registry/` no projeto

O diretorio `models/registry/` continua existindo, mas com papel deliberadamente secundario.

Ele serve para:

- guardar manifests locais de apoio
- facilitar debug
- apoiar estudo do fluxo
- manter um espelho local do ultimo treino

Ele nao deve ser tratado como source of truth principal quando existir MLflow Registry remoto.

Hoje o projeto gera, por exemplo:

- `models/registry/latest-run.json`
- `models/registry/<model-name>-<timestamp>.json`

Esses arquivos ajudam a enxergar rapidamente o resultado da ultima execucao, mas a governanca oficial deve viver no MLflow.

## Como pensar em estagios

Mesmo que o projeto ainda nao esteja promovendo estagios automaticamente, vale adotar desde ja o modelo mental correto:

- `None`: versao criada, ainda sem promocao
- `Staging`: versao candidata, pronta para validacao ampliada
- `Production`: versao aprovada para uso produtivo
- `Archived`: versao aposentada

Em muitas empresas, essa promocao e ligada a criterios como:

- metricas minimas
- ausencia de regressao em comparacao ao baseline
- validacao de contrato
- aprovacao manual
- resultado de monitoramento ou smoke tests

## Como usar na pratica

### Registro automatico no treino

Hoje, ao rodar:

```bash
make train
```

o projeto tenta registrar uma nova versao do modelo automaticamente.

Se o registry remoto estiver disponivel, o retorno do treino inclui uma versao real.

Se o backend nao suportar registry, o treino nao falha; ele responde com `registration_status` adequado e preserva o restante da execucao.

### O que observar no retorno do treino

Os campos mais importantes sao:

- `run_id`
- `artifact_uri`
- `model_name`
- `model_version`
- `registration_status`
- `registration_error`

Isso permite diferenciar claramente:

- treino que apenas rodou
- treino que rodou e gerou artifact
- treino que rodou, gerou artifact e registrou versao

## Padrões de mercado que valem seguir

- use nome de modelo estavel e semanticamente claro
- promova versoes, nunca sobrescreva conceito de modelo
- mantenha criterios de promocao fora da cabeca das pessoas e dentro do processo
- ligue sempre a versao registrada a metricas e artifacts explicativos
- trate registry como camada de governanca, nao apenas como deposito

## Hacks praticos que mudam o jogo

- nunca use o registry para guardar "qualquer run"; registre apenas o que faz sentido comparar e promover
- use campos de retorno do treino para alimentar CI/CD e processos de aprovacao
- deixe um manifesto local em `models/registry/` para acelerar troubleshooting
- diferencie claramente modelo candidato de modelo promovido
- quando o projeto amadurecer, faca `predict.py` consumir modelo por estagio ou alias, nao por arquivo solto

## O que nunca esquecer

- registry sem tracking forte vira casca vazia
- versao sem metrica e evidencia nao deveria ser promovida
- promocao automatica cedo demais cria risco operacional
- backend local ajuda a aprender, mas governanca real pede backend remoto persistente
- arquivo serializado em disco nao substitui uma versao registrada

## Como esta documentacao se conecta ao codigo

- nome e configuracao do modelo: `src/meu_projeto_ds/config.py`
- tentativa de registro: `src/meu_projeto_ds/models/tracking.py`
- fluxo de treino e retorno de versao: `src/meu_projeto_ds/models/train.py`
- manifests locais de apoio: `models/registry/README.md` e `models/registry/latest-run.json`
- automacao futura de promocao: `.github/workflows/cd-model.yml`

## Proximo passo natural

Depois de entender registry, o proximo salto e documentar e implementar:

- criterios de promocao
- operacao em CI/CD
- consumo de modelos por estagio na inferencia

Esse material deve entrar em `docs/mlflow-operacao.md`.
