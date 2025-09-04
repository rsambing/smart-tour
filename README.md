# SmartTour Angola 🇦🇴

**Sistema de Análise de Turismo Sustentável para Angola**

Desenvolvido para o FTL Bootcamp Hackathon - Uma solução completa para descentralizar o turismo em Angola através de análise de dados e rotas de ecoturismo sustentável.

![SmartTour](https://img.shields.io/badge/SmartTour-v1.0.0-red)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![GUI](https://img.shields.io/badge/GUI-PySide6-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📝 Descrição do Projeto

O **SmartTour** é uma aplicação desktop inovadora que combina:
- 📊 **Análise de dados turísticos** em tempo real
- 🌱 **Avaliação de sustentabilidade** de sítios ecológicos
- 🗺️ **Otimização de rotas** de ecoturismo
- 📈 **KPIs e métricas** de performance
- 🎯 **Alinhamento com ODS** (Objetivos de Desenvolvimento Sustentável)

### 🎯 Objetivo Principal
Promover o **turismo sustentável** e a **descentralização turística** em Angola, oferecendo ferramentas analíticas para:
- Gestores de turismo
- Operadoras turísticas
- Órgãos governamentais
- Pesquisadores e academicos

## ⚙️ Requisitos Técnicos

### Sistema
- **Python**: 3.12+
- **Sistema Operacional**: Windows, macOS, Linux
- **Memória RAM**: 4GB mínimo, 8GB recomendado
- **Espaço em disco**: 500MB

### Dependências Python
```bash
pip install -r requirements.txt
```

**Principais dependências:**
- `PySide6` - Interface gráfica moderna
- `pandas` - Manipulação de dados
- `numpy` - Computação numérica  
- `matplotlib` - Visualizações estáticas
- `seaborn` - Gráficos estatísticos
- `plotly` - Visualizações interativas

## 🚀 Instalação e Execução

### 1. Clone o Repositório
```bash
git clone [url-do-repositorio]
cd hackathon-1
```

### 2. Instale Dependências
```bash
pip install -r requirements.txt
```

### 3. Teste a Instalação
```bash
python test_smarttour.py
```

### 4. Execute a Aplicação
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
smart-tour/
├── docs/                           # Documentação do projeto
│   ├── requirements.txt            # Dependências principais
│   └── solucoes.md                 # Soluções propostas / guia interno
│
├── logs/                           # Logs do sistema
│   └── smarttour.log
│
├── templates/                      # Templates HTML (modo web)
│   ├── index.html                  # Página inicial (upload/inputs)
│   └── results.html                # Página de resultados/relatórios
│
├── uploads/                        # Arquivos de entrada (datasets)
│   ├── Eco_Sites__preview_.csv
│   └── Visitors_by_Province__preview_.csv
│
├── launcher.py                     # Script de inicialização principal
├── smarttour_core.py               # (Nucleo do funcionamento do desktop)
├── smarttour_web.py                # Interface web (Flask)
├── smarttour_integrated.py         # Versão integrada (no terminal)
├── smarttour_desktop_clean.py      # Variante desktop estável/testada
├── smarttour_angola_report.html    # Relatório gerado
├── README.md                       # Descrição do projeto
```

## 🎯 Funcionalidades Principais

### 📊 Análise de Dados Turísticos
- **Visitantes por Província**: Análise temporal e geográfica
- **Sazonalidade**: Identificação de épocas alta/baixa
- **Perfil de Visitantes**: Nacional vs. Internacional
- **Duração de Estadia**: Métricas de permanência

### 🌱 Avaliação de Sustentabilidade
- **Índice de Fragilidade**: Classificação de sítios ecológicos
- **Capacidade de Carga**: Limite sustentável de visitantes
- **Score de Sustentabilidade**: Métrica de 0-10
- **Recomendações**: Ações para melhoria

### 🗺️ Otimização de Rotas
- **Rotas Sustentáveis**: Baseadas em critérios ecológicos
- **Otimização de Distância**: Minimização de deslocamentos
- **Capacidade Integrada**: Consideração de limites de visitantes
- **Análise de Custos**: Estimativas econômicas

### 📈 KPIs e Dashboards
- **KPIs Turísticos**: Visitantes, crescimento, sazonalidade
- **KPIs Sustentabilidade**: Fragilidade, capacidade, score
- **KPIs Econômicos**: Receitas, distribuição, impacto
- **Visualizações Interativas**: Gráficos e dashboards

### Fontes de Dados
- **Visitantes por Província**: Dados temporais de turismo
- **Sítios Ecológicos**: Localização, capacidade, fragilidade
- **Reviews**: Avaliações e feedback (futuro)
- **Reservas**: Dados de ocupação (futuro)
- **Impacto Ambiental**: Métricas de sustentabilidade (futuro)

### KPIs Principais

#### 🎯 Turismo
- **Visitantes Anuais**: Volume total estimado
- **% Estrangeiros**: Participação internacional
- **Estadia Média**: Duração das visitas
- **Variação Sazonal**: Diferença época alta/baixa
- **Taxa de Crescimento**: Crescimento anual por província

#### 🌱 Sustentabilidade  
- **% Sites Sustentáveis**: Sítios com baixa fragilidade
- **Score Médio**: Pontuação de sustentabilidade (0-10)
- **Capacidade Total**: Capacidade diária agregada
- **Províncias Cobertas**: Distribuição geográfica

#### 💰 Econômico
- **Receita Estimada**: Potencial econômico anual
- **Taxa Média**: Preço médio por sítio
- **Distribuição**: Equidade entre províncias

## 🎯 Alinhamento com ODS

### Objetivos de Desenvolvimento Sustentável
- **ODS 8**: Trabalho Decente e Crescimento Econômico
- **ODS 11**: Cidades e Comunidades Sustentáveis
- **ODS 12**: Consumo e Produção Responsáveis  
- **ODS 13**: Ação contra Mudança Climática
- **ODS 15**: Vida Terrestre

### Contribuições Específicas
- 📈 **Crescimento Econômico**: Diversificação do turismo
- 🏛️ **Desenvolvimento Regional**: Descentralização
- 🌱 **Turismo Responsável**: Práticas sustentáveis
- 🌍 **Conservação**: Proteção de ecossistemas
- 📚 **Conhecimento**: Dados para tomada de decisão

## 🧪 Testes e Validação

### Execute os Testes
```bash
python test_smarttour.py
```

### Validações Incluídas
- ✅ Carregamento de dados
- ✅ Processamento de análises
- ✅ Geração de KPIs
- ✅ Criação de visualizações
- ✅ Exportação de relatórios
- ✅ Análise por província

## 📄 Relatórios e Exportação

### Tipos de Relatório
- **HTML Executivo**: Relatório completo interativo
- **Análise Provincial**: Relatório específico por região
- **Dashboard KPIs**: Métricas principais
- **Visualizações**: Gráficos exportáveis

## 👥 Equipa de Desenvolvimento

**Grupo 2 - FTL Bootcamp**
- 👑 **Team Leader**: Reinaldo Sambinga
- 👥 **Team**:Alberto Pessela, Manuel Joaquim, Joao Antonio, Jose Poba, Maria Jose, Sérgio Chisevo
- 🎯 **Objetivo**: Desenvolver solução inovadora para turismo sustentável
- 📅 **Prazo**: Hackathon FTL Bootcamp
- 🏆 **Meta**: Sistema completo e funcional

### Suporte Técnico
- 📧 **Email**: [reinaldogts252@gmail.com]
- 📱 **GitHub Issues**: Para bugs e sugestões
- 📚 **Documentação**: Wiki do projeto

## 🎉 Agradecimentos

- **FTL Bootcamp**: Pela oportunidade e desafio
- **Comunidade Python**: Bibliotecas e ferramentas
- **Angola Tourism Board**: Inspiração e contexto

---

<div align="center">

**SmartTour Angola** 🇦🇴  
*"Transformando dados em turismo sustentável"*

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python&logoColor=white)](https://python.org)
[![GUI with PySide6](https://img.shields.io/badge/GUI-PySide6-green?logo=qt&logoColor=white)](https://wiki.qt.io/Qt_for_Python)
[![Data Analysis](https://img.shields.io/badge/Analysis-Pandas-red?logo=pandas&logoColor=white)](https://pandas.pydata.org)

**Desenvolvido para o FTL Bootcamp Hackathon**

</div>
