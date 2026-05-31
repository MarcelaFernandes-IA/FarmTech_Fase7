# 🌾 Classificação de Sementes de Trigo — FASE 04 / CTWP / Capítulo 3

Este repositório contém a atividade de Machine Learning utilizando o **Seeds Dataset**, estruturada conforme a metodologia **CRISP-DM**. O objetivo é classificar três variedades de trigo (Kama, Rosa e Canadian) a partir de suas características físicas.

---

## 📁 Estrutura do Repositório
- `seeds_classification.ipynb` — Notebook com toda a análise, modelagem, otimização e resultados finais.
- `README.md` — Documento explicativo com resumo, metodologia e conclusões principais.

---

## 📌 Metodologia (CRISP-DM)

### **1. Entendimento do Negócio**
Cooperativas agrícolas de pequeno porte realizam a classificação de grãos manualmente, processo sujeito a erros humanos. O objetivo é automatizar essa tarefa usando modelos de Machine Learning.

### **2. Entendimento dos Dados**
Foram utilizadas 210 amostras de sementes com sete características físicas, além da classe (variedade). Dados sem valores ausentes e bem distribuídos entre as classes.

### **3. Preparação dos Dados**
- Exploração estatística e visual
- Padronização (StandardScaler)
- Divisão treino/teste (70/30)

### **4. Modelagem**
Modelos aplicados:
- K-Nearest Neighbors (KNN)
- Random Forest
- Regressão Logística Multinomial

### **5. Avaliação**
Avaliações por:
- Acurácia
- Precisão, Recall e F1-score
- Matriz de confusão
- Comparação entre baseline e modelos otimizados

---

## 📊 Desempenho dos Modelos
Foram avaliados três algoritmos de classificação: **KNN**, **Random Forest** e **Regressão Logística Multinomial**.

Na etapa inicial (baseline), os modelos apresentaram acurácias entre **84% e 90%**. Após a otimização com **GridSearchCV**, houve melhora adicional, principalmente no modelo **KNN**, que atingiu acurácia aproximada de **90%** no conjunto de teste.

As matrizes de confusão mostram que os erros ocorrem principalmente entre as variedades **Kama** e **Canadian**, indicando similaridade física entre grãos dessas classes. Já a variedade **Rosa** apresenta maior separação e menor taxa de confusão.

Do ponto de vista do negócio, isso significa que modelos de Machine Learning podem automatizar a classificação com alta precisão usando apenas medições físicas simples, reduzindo tempo, custo e erros humanos em pequenas cooperativas agrícolas.

---

## 🧾 Conclusões Gerais
- O conjunto de dados mostrou-se adequado para modelos supervisionados, com boa separação entre classes.
- Todos os modelos atingiram desempenho satisfatório, sendo o **KNN** o que apresentou melhor performance após otimização.
- A metodologia **CRISP-DM** foi aplicada integralmente, garantindo estrutura e clareza no desenvolvimento do projeto.
- O estudo comprova a viabilidade de automatizar a classificação de grãos em ambientes agrícolas reais.

---

## 📎 Autor
Atividade desenvolvida como parte da **FASE 04 / CTWP / Capítulo 3**.

---

## 🔗 Como visualizar
Clique no arquivo `seeds_classification.ipynb` para ver a análise completa, gráficos, código e resultados finais.

