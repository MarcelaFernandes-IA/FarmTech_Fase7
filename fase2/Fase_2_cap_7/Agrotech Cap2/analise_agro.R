# MARCELA_AMORIM_FERNANDES_RM566995_fase2_cap7
# Análise exploratória de base agro (synthetic didática)
# Pacotes necessários: readxl, ggplot2, dplyr

# Instalar pacotes (descomente se precisar)
# install.packages(c('readxl','ggplot2','dplyr'))

library(readxl)
library(ggplot2)
library(dplyr)

# 1) Ler a base (ajuste o caminho se necessário)
base <- read_excel('base_agro.xlsx')

# 2) Conferir estrutura
str(base)
head(base)

# Garantir que a variável ordinal esteja ordenada corretamente
base$porte_fazenda <- factor(base$porte_fazenda,
                             levels = c('Pequena','Média','Grande','Muito grande'),
                             ordered = TRUE)

# ==============================
# ESCOLHA DA VARIÁVEL QUANTITATIVA: rendimento_t_ha
# ==============================

x <- base$rendimento_t_ha

# Medidas de tendência central
media <- mean(x, na.rm = TRUE)
mediana <- median(x, na.rm = TRUE)
# Moda (pode haver múltiplas; aqui escolhemos a de maior frequência)
moda <- as.numeric(names(which.max(table(x))))

# Medidas de dispersão
variancia <- var(x, na.rm = TRUE)
desvio_padrao <- sd(x, na.rm = TRUE)
amplitude <- max(x, na.rm = TRUE) - min(x, na.rm = TRUE)
iqr_val <- IQR(x, na.rm = TRUE)
cv <- desvio_padrao / media  # coeficiente de variação

# Medidas separatrizes (quartis, decis, percentis)
quartis <- quantile(x, probs = c(0.25, 0.5, 0.75), na.rm = TRUE, names = TRUE)
decis <- quantile(x, probs = seq(0.1, 0.9, by = 0.1), na.rm = TRUE, names = TRUE)
percentis <- quantile(x, probs = seq(0.01, 0.99, by = 0.01), na.rm = TRUE, names = TRUE)

# Imprimir resumo
cat('== Tendência central ==\n')
cat('Média:', media, '\n')
cat('Mediana:', mediana, '\n')
cat('Moda:', moda, '\n\n')

cat('== Dispersão ==\n')
cat('Variância:', variancia, '\n')
cat('Desvio padrão:', desvio_padrao, '\n')
cat('Amplitude:', amplitude, '\n')
cat('IQR:', iqr_val, '\n')
cat('CV:', cv, '\n\n')

cat('== Quartis ==\n'); print(quartis)
cat('\n== Decis ==\n'); print(decis)
cat('\n== Percentis (1% a 99%) ==\n'); print(percentis)

# Análise gráfica da variável quantitativa
# Histograma com densidade
g_hist <- ggplot(base, aes(x = rendimento_t_ha)) +
  geom_histogram(binwidth = 0.25, fill = 'grey80', color = 'black') +
  geom_density(aes(y=..density..)) +
  labs(title = 'Histograma e densidade: rendimento (t/ha)',
       x = 't/ha', y = 'Densidade')

# Boxplot
g_box <- ggplot(base, aes(y = rendimento_t_ha)) +
  geom_boxplot(fill = 'grey85') +
  labs(title = 'Boxplot: rendimento (t/ha)', y = 't/ha')

# Salvar gráficos
ggsave('grafico_hist_rendimento.png', plot = g_hist, width = 7, height = 4, dpi = 150)
ggsave('grafico_box_rendimento.png', plot = g_box, width = 5, height = 4, dpi = 150)

# ==============================
# ESCOLHA DA VARIÁVEL QUALITATIVA: porte_fazenda (ordinal)
# ==============================

# Gráfico de barras
g_bar <- ggplot(base, aes(x = porte_fazenda)) +
  geom_bar(fill = 'grey70', color = 'black') +
  labs(title = 'Distribuição do porte das fazendas',
       x = 'Porte (ordinal)', y = 'Contagem')

ggsave('grafico_bar_porte.png', plot = g_bar, width = 6, height = 4, dpi = 150)

# Tabela de frequências (absoluta e relativa)
freq_abs <- table(base$porte_fazenda)
freq_rel <- prop.table(freq_abs)

cat('\n== Frequências (porte_fazenda) ==\n')
print(freq_abs)
cat('\n== Frequências relativas ==\n')
print(round(100*freq_rel, 2))
