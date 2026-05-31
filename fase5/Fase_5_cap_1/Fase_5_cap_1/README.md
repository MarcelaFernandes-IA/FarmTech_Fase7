# **Projeto FarmTech Solutions \- Fase 5**

Este repositório contém a solução completa para o desafio da Fase 5, integrando Ciência de Dados (Machine Learning) e Infraestrutura em Nuvem (AWS).

## **👥 Integrantes do Grupo**

* **Adrison Magalhães** \- RM: rm568165  
* **Sabrina Pereira Santo** \- RM: rm568170  
* **Anna Carolina Martins Souza** \- RM: rm566692  
* **Juan Battagin Barrocal** \- RM: rm567410  
* **Marcela Amorim Fernandes** \- RM: rm566995

## **🌾 Entrega 1: Inteligência Artificial e Análise de Dados**

Nesta etapa, utilizamos o dataset crop\_yield.csv para criar um modelo preditivo capaz de estimar o rendimento das colheitas com base em fatores climáticos.

### **📈 Resumo do Desenvolvimento:**

1. **Análise Exploratória (EDA):** Identificamos correlações entre temperatura, umidade e rendimento.  
2. **Clusterização (K-Means):** Agrupamos as safras por comportamento e identificamos anomalias (outliers).  
3. **Modelagem Preditiva:** Testamos 5 algoritmos de regressão.  
4. **Resultado Final:** O modelo **Random Forest Regressor** foi o vencedor, apresentando uma precisão de aproximadamente **0.99**.

### **🔗 Documentos da Entrega 1:**

* **Notebook:** [Cap 1 - FarmTech.ipynb](./Cap%201%20-%20FarmTech.ipynb)
* **Vídeo de Demonstração:** [Vídeo de Demonstração](https://www.youtube.com/watch?v=6xQCZidoCVo)

## **☁️ Entrega 2: Planejamento de Infraestrutura AWS**

Nesta etapa, realizamos o levantamento de custos para hospedar nossa solução em uma infraestrutura escalável na nuvem.

### **💰 Comparativo de Custos (AWS Pricing Calculator)**

*Configuração: Instância EC2 (2 vCPUs, 1 GiB RAM), 50 GB de Armazenamento EBS.*

| Região | Custo Estimado Mensal (USD) |
| :---- | :---- |
| **Virgínia do Norte (us-east-1)** | $ \[Preencher Valor\] |
| **São Paulo (sa-east-1)** | $ \[Preencher Valor\] |

### **⚖️ Justificativa de Escolha e Aspectos Legais**

* **Decisão:** Escolhemos a região de **\[Colega: Preencher a Escolha\]**.  
* **Justificativa Técnica:** \[Colega: Explicar sobre latência e custo\].  
* **Conformidade Legal:** Em caso de restrições legais sobre o armazenamento de dados sensíveis no exterior, a opção por **São Paulo (Brasil)** é mandatória para garantir a soberania dos dados e conformidade com a LGPD.

### **🔗 Documentos da Entrega 2:**

## ☁️ Entrega 2: Planejamento de Infraestrutura AWS

### 🔗 Documentos da Entrega 2:

- **Vídeo de Demonstração (AWS):** [YouTube](https://www.youtube.com/watch?v=6xQCZidoCVo)


## **🛠️ Como Executar o Projeto**

1. Abra o arquivo .ipynb no Google Colab.  
2. Certifique-se de que o arquivo crop\_yield.csv está acessível no caminho definido no código.  
3. Execute as células em ordem para visualizar as análises e o treinamento dos modelos.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAYCAYAAAARfGZ1AAAByElEQVR4Xu2UO0sDURCF8xBFRUVEAnltEiLRFIJoIVikEgvB1kfEFBaCnYWopUUEaxtBBXvBykIQFATBUqzEKn/Axj+g38nu6s2aaGJi54Fhd87MnZl7Mhuf7x9/gEAikcjF4/EtbCUUCnV7E36NWCw2l0wmR312k4JlWcfpdLrXm9cwotFoJ9MeUnRHPo3CFL/Gn/TmlkFwDLvBXrE3PUm+5fmElSh2KhlIDSgfP8XkIb3ztFQcbryiqBeaBnt2ruwiIBnUBFvC9xsxDZbHDnQjk69AOBzuIukIu2CKfjMWiUQG4C69MfwRhtnNZDI9Zv4XONe74/AebtCMUWAYeyR+lkql+sQx6RDcmiZWce9AFSA4Ja0lgTcGv6oYxRbkS2/8dT11K/gZDeA99wGCG1X0bqPIrG5EbFF+Nptt533fsn94165YxUHj3Cfc9bLs7Thx3s81LbbZ1A7X0NuPvwxfQqoJM78huHpz3XmTp2kG/kEravINoYbeajotTbUVJl83vttvNXV+sLzJ1w0OSvD7KvsdhC+axWlW+PEzFySB89W9OAXK/yfS383Bz1n2Z19M2Lu8zeZ0mHWagqRSQ21MSwv/o6V4B9vAdlXL3MiNAAAAAElFTkSuQmCC>

## **🌾 Entrega : Comparação de custos AWS**

Para esta etapa, foi utilizada a AWS Pricing Calculator para estimar o custo mensal de uma infraestrutura Linux simples, em modalidade On-Demand, destinada a hospedar uma API de recepção de dados dos sensores e executar o modelo de Machine Learning desenvolvido na Entrega 1. A cobrança On-Demand foi escolhida por estar alinhada ao enunciado, que solicita simulação com uso de 100% sob demanda.

A configuração solicitada foi de 2 CPUs, 1 GiB de memória, até 5 Gigabit de rede e 50 GB de armazenamento. Foi identificada uma instância EC2 e adotada na configuração usando uma família T3, que oferece 2 vCPUs, 2 GiB de memória, armazenamento EBS e rede de até 5 gigabits. Também foi considerado armazenamento de 50 GB em EBS.

Foram comparadas duas regiões:

South America (São Paulo)

US East (N. Virginia)

Estes foram os custos gerados:

![img_1.png](img_1.png)
![img_2.png](img_2.png)

Apesar de a região de N. Virginia normalmente apresentar menor custo, a escolha recomendada para este cenário é São Paulo, pois a aplicação precisa acessar rapidamente os dados dos sensores e há restrições legais para armazenamento no exterior. Além disso, a AWS recomenda a utilização de regiões mais próximas dos usuários para reduzir latência e melhorar o desempenho.
