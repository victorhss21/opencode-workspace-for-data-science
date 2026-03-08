Aqui vai um roadmap prático para usar o OpenCode com mais eficiência em projetos de ciência de dados.

## **Roadmap**

- Comece pelo contexto certo: sempre informe objetivo de negócio, tipo/volume dos dados, métrica principal, restrições de tempo/memória e formato de entrega.
- Estruture o projeto antes de acelerar: use algo como `data/`, `notebooks/`, `src/`, `models/`, `tests/`, `reports/`, `configs/`; deixe notebook para exploração e mova lógica estável para `src/`.
- Trabalhe em ciclos curtos: `EDA -> limpeza -> baseline -> otimização -> validação -> empacotamento`; evite pedir “faça tudo” em uma única rodada.
- Use o OpenCode para tarefas fechadas e verificáveis: “otimize memória”, “adicione testes”, “converta notebook em pipeline”, “compare modelos com foco em latência”.
- Sempre peça saída operacional: arquivos alterados, racional das mudanças, como validar e riscos assumidos.

## **Como usar por fase**

### **EDA**
- Peça análise de schema, missing, outliers, cardinalidade, leakage e drift inicial.
- Exemplo: `Analise o dataset e priorize os principais problemas de qualidade de dados por impacto no modelo`.

### **Preparação**
- Peça pipelines reproduzíveis, funções puras e transformações vetorizadas.
- Solicite consistência entre treino e inferência e checagem de tipos.

### **Modelagem**
- Comece com baseline simples e interpretável.
- Depois peça comparação com modelos mais fortes, sempre com critério claro: acurácia, custo, tempo, interpretabilidade.

### **Avaliação**
- Defina a validação correta: temporal, estratificada, por grupo ou K-fold.
- Peça métricas técnicas e métricas de negócio.

### **Produção**
- Solicite scripts CLI, configuração por arquivo, testes mínimos, logs e documentação de execução.

## **Como extrair mais performance**

### **Dados**
- Peça downcast numérico, tipos categóricos, leitura seletiva de colunas, processamento em lotes.
- Quando fizer sentido, peça `polars`, `pyarrow`, `dask` ou `pyspark`.

### **Código**
- Peça profiling antes de otimizar.
- Exemplo: `Identifique os 3 maiores gargalos de CPU/memória e aplique as correções de maior ROI`.

### **Treino**
- Use amostragem para iteração rápida, early stopping e tuning com orçamento fixo.
- Evite buscas exaustivas sem limite de tempo.

### **Reprodutibilidade**
- Peça seeds fixas, configs centralizadas, ambiente reproduzível e versionamento de artefatos.

## **Prompts que funcionam bem**

- `Leia o projeto e proponha um plano de refatoração focado em performance e reprodutibilidade.`
- `Converta este notebook em módulos Python testáveis.`
- `Otimize este preprocessing para reduzir uso de memória sem alterar o resultado.`
- `Implemente um baseline e compare com uma opção mais forte, justificando custo-benefício.`
- `Adicione testes para garantir consistência entre treino e inferência.`

**Erros a evitar**

- Pedidos vagos demais.
- Otimizar modelo antes de resolver leakage e qualidade dos dados.
- Deixar regra crítica só em notebook.
- Não definir métrica de sucesso.
- Não pedir validação reproduzível.

## **Plano de maturidade**

### **Nível 1**
- EDA, limpeza, gráficos, baseline e documentação.

### **Nível 2**
- Modularização de notebooks, pipelines, testes e benchmarks.

### **Nível 3**
- Profiling, tuning com orçamento, redução de memória e paralelismo.

### **Nível 4**
- Padronização, CI, monitoramento e inferência reproduzível.