# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="img/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

---

## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/adrison-magalh%C3%A3es-72bab0231">Adrison Magalhães</a>  
- <a href="https://www.linkedin.com/in/anna-carolina">Anna Carolina Martins</a>
- <a href="https://www.linkedin.com/in/juan-barrocal">Juan Barrocal</a>
- <a href="https://www.linkedin.com/in/marcelaamorimfernandes">Marcela Amorim</a>
- <a href="https://www.linkedin.com/in/sabrina-santos">Sabrina Santos</a>

---

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni-22525519b">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato">Andre Godoi</a>

---

# 🧠 Detecção de Objetos com YOLOv8 - FarmTech Solutions

## 📌 Objetivo

Este projeto tem como objetivo desenvolver um modelo de visão computacional capaz de identificar dois objetos distintos: **lápis** e **colher**, simulando uma aplicação prática no contexto da **FarmTech Solutions**, onde a detecção automática de objetos pode contribuir para automação de processos e controle operacional.

---

## 📓 Como acessar o projeto

Todo o desenvolvimento, código executado e análise detalhada estão documentados no notebook Jupyter. Para acessar:

1. Clique no link abaixo para abrir o notebook no Google Colab
2. Faça login com sua conta Google
3. Execute as células na ordem, de cima para baixo

👉 [Abrir Notebook no Google Colab](https://colab.research.google.com/drive/1SNSs3flTVygQw-6f37BiEzRm-6o5QPau?usp=sharing)

> O notebook contém todo o passo a passo das Entregas 1 e 2, incluindo gráficos de desempenho, imagens processadas e conclusões.

---

## 📊 Dataset

O dataset foi composto por **80 imagens**, sendo:
- 40 imagens de lápis
- 40 imagens de colher

👉 https://drive.google.com/drive/folders/1DFq8NsVW22mhh6OKGkzmugJVjyhKaHQ9?usp=sharing

### 🔀 Divisão dos dados:
- **Treino:** 32 imagens por classe
- **Validação:** 4 imagens por classe
- **Teste:** 4 imagens por classe

As imagens foram organizadas em estrutura compatível com YOLO e armazenadas no Google Drive.

---

## 🏷️ Rotulação

As imagens de treino e validação foram rotuladas utilizando a ferramenta:

👉 https://www.makesense.ai/

Formato de saída:
- YOLO (bounding boxes normalizadas)

---

## ⚙️ Tecnologias utilizadas

- Python
- Google Colab
- YOLOv8 (Ultralytics)
- TensorFlow / Keras
- Google Drive

---

## 🚀 Entrega 1 — YOLOv8 Customizado

## 📌 Objetivo da Entrega 1

Desenvolver um modelo customizado com YOLOv8 capaz de detectar e localizar lápis e colheres em imagens, treinado com dataset próprio e rotulado manualmente.

---

### Treinamento do modelo

Foram realizados dois experimentos:

| Experimento | Épocas |
|------------|--------|
| Modelo 1   | 30     |
| Modelo 2   | 60     |

O objetivo foi avaliar o impacto do número de épocas no desempenho do modelo.

### 📈 Resultados

- O modelo apresentou boa convergência durante o treinamento
- O mAP50 atingiu aproximadamente **0.644**
- A precisão e recall evoluíram ao longo das épocas
- Imagens dos resultados: https://drive.google.com/drive/folders/1BTE3MwAz5SK9t7q3ouu2Bo-lSFRs8oW5?usp=drive_link

### 🔍 Principais observações:
- Melhor desempenho na detecção de **colheres**
- Maior dificuldade na detecção de **lápis**
- Ocorrência de:
  - detecções duplicadas
  - baixa confiança em alguns casos
  - imprecisão nas bounding boxes

### 🧪 Testes

O modelo foi aplicado em imagens não vistas anteriormente.

- Boa capacidade de generalização
- Identificação correta na maioria dos casos
- Pequenas falhas esperadas devido ao tamanho reduzido do dataset
- Gráficos: https://drive.google.com/file/d/13-NvK5ZVvzr5N5UoXoYh4eKY0Rk5dbr1/view?usp=sharing
- Matriz de confusão: https://drive.google.com/file/d/1Kvl7-zD1KkKhIcuPDOiussPo6ohJIz02/view?usp=sharing

### 🎥 Vídeo demonstrativo — Entrega 1

👉 https://youtu.be/8eaqSKlxQVA

---

## 📊 Entrega 2 — Comparação entre Abordagens

## 📌 Objetivo da Entrega 2

Comparar três abordagens de detecção/classificação de objetos usando o mesmo dataset
de **lápis** e **colher**, avaliando precisão, facilidade de uso e tempo de inferência.

---

### 1️⃣ YOLOv8 Customizado (Entrega 1)

O modelo foi treinado do zero com o dataset rotulado manualmente no MakeSense.ai,
utilizando 64 imagens de treino (32 por classe), 16 para validação e testado em 8 imagens nunca vistas.

**Resultados:**
- mAP50: **0.644**
- Precisão: 0.659 | Recall: 0.616
- Tempo de inferência: ~2.06ms por imagem (GPU)
- Melhor desempenho na detecção de colheres
- Maior dificuldade com lápis (objeto mais fino e com menos variação visual)

**Observações:**
- Exigiu rotulação manual com bounding boxes
- Requer configuração de dataset no formato YOLO
- Capaz de **localizar** o objeto na imagem (desenha a caixa)
- Dois treinos realizados: 30 e 60 épocas — o de 60 apresentou ganhos marginais

---

### 2️⃣ YOLO Padrão (pré-treinado no COCO)

O modelo YOLOv8n foi utilizado sem nenhum treino adicional, apenas com os pesos
pré-treinados nas 80 classes do dataset COCO.

**Resultados:**
- Lápis: **0 detecções** — a classe não existe no COCO
- Colher: detectou corretamente em apenas **1 de 8 imagens**, confundindo com escova de dente e faca
- Tempo médio de inferência: **0.2401s**

**Observações:**
- Facilíssimo de usar — apenas 3 linhas de código
- Zero configuração ou treino necessário
- **Ineficaz para objetos fora das 80 classes padrão**
- Demonstra claramente a necessidade de customização para casos específicos

---

### 3️⃣ CNN do Zero (TensorFlow/Keras)

Uma rede neural convolucional foi construída do zero para classificar as imagens
em duas classes: lápis e colher.

**Arquitetura:**
- 3 blocos Conv2D + MaxPooling (32 → 64 → 128 filtros)
- Dense(128) + Dropout(0.2) + Softmax
- Data augmentation: RandomFlip e RandomRotation
- 20 épocas de treino

**Resultados:**
- Acurácia no teste: **87.50% (7/8 imagens)**
- 1 erro: colher classificada como lápis (72.79% de confiança errada)
- Acertos: 3 colheres e 4 lápis identificados corretamente
- Tempo médio de inferência: **~0.0719s por imagem**

**Observações:**
- Não requer rotulação com bounding boxes — apenas organização em pastas
- Mais simples de implementar que o YOLO customizado
- **Classifica** a imagem inteira, mas **não localiza** o objeto (sem caixa)

### ⚠️ Análise do erro da CNN

A única imagem classificada incorretamente foi `teste_colher_01.jpg`,
identificada como lápis com 72.79% de confiança.

A imagem contém 6 colheres dispostas paralelamente, o que difere do padrão
visto durante o treino, onde as imagens de colher geralmente mostravam
1 ou poucos objetos. A disposição paralela de múltiplas colheres pode ter
criado um padrão visual semelhante ao de vários lápis agrupados, confundindo
o modelo.

Isso evidencia uma limitação da CNN: o modelo é sensível à quantidade e
disposição dos objetos na imagem, e pode falhar quando a foto de teste
tem uma composição muito diferente das imagens de treino.

---

### 📋 Tabela Comparativa Final

| Critério | YOLOv8 Customizado | YOLO Padrão | CNN do Zero |
|---|---|---|---|
| **Precisão** | mAP50: 0.644 | Muito baixa (falhou no lápis, errou colher) | 87.50% |
| **Localiza o objeto** | ✅ Sim (bounding box) | ✅ Sim (bounding box) | ❌ Não (só classifica) |
| **Facilidade de uso** | ⭐⭐ Média | ⭐⭐⭐ Alta | ⭐⭐ Média |
| **Rotulação necessária** | ✅ Sim (bounding boxes) | ❌ Não | ❌ Não (só pastas) |
| **Tempo de treino** | ~1.3 min (30 épocas) / ~1.8 min (60 épocas) | Sem treino | ~20 segundos |
| **Tempo de inferência** | ~2ms | ~0.24s | ~0.07s por imagem |
| **Funciona para objetos específicos** | ✅ Sim | ❌ Não | ✅ Sim |

---

### 🧠 Conclusão

Cada abordagem tem seu contexto ideal:

- **YOLO Padrão** é a solução mais rápida de implementar, mas completamente ineficaz
para objetos fora das suas 80 classes. Não é indicado para casos específicos como o deste projeto.

- **CNN do Zero** apresentou a melhor acurácia de classificação (87.50%) com menor
complexidade de implementação — sem necessidade de bounding boxes. Porém, não informa
*onde* o objeto está na imagem, apenas *o que* é.

- **YOLOv8 Customizado** é a abordagem mais completa: detecta e localiza os objetos
com bounding boxes, sendo ideal para aplicações práticas como automação e controle
de qualidade na FarmTech Solutions. Exige mais esforço de preparação (rotulação),
mas entrega o resultado mais rico e aplicável.

> Para o contexto da FarmTech Solutions, onde é necessário identificar e localizar
> objetos automaticamente em imagens, o **YOLOv8 Customizado** é a solução mais
> adequada, desde que se invista na criação de um dataset rotulado de qualidade.

---

## 🎥 Vídeo demonstrativo — Entrega 2

👉 https://www.youtube.com/watch?v=bQXq0_H5SSM

---

## 👥 Autores

- **Marcela Amorim Fernandes** — RM: 566995 (Entrega 1 — YOLOv8 Customizado)
- **Anna Carolina Martins Souza** — RM: 566692 (Entrega 2 — YOLO Padrão e CNN do Zero)
