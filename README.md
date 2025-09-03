# SmartTour Angola 🇦🇴

**Sistema Integrado de Análise de Turismo Sustentável**

Sistema completo com **3 interfaces diferentes**: Desktop, Web e Terminal para análise de turismo sustentável em Angola.

![SmartTour](https://img.shields.io/badge/SmartTour-v3.0-red) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Status](https://img.shields.io/badge/Status-MultiInterface-green)

## 🌟 Características Principais

- **🎯 Análise Completa**: KPIs de turismo, sustentabilidade e econômicos
- **🖥️ Interface Desktop**: Aplicação nativa com tkinter e tema escuro
- **🌐 Interface Web**: App web moderno com Flask e design responsivo
- **� Visualizações**: Gráficos interativos com Plotly
- **📄 Relatórios HTML**: Exportação automática de relatórios elegantes
- **🎨 Design Ecológico**: Tema escuro com verde e dourado

## 🚀 Como Usar

### Opção 1: Launcher (Recomendado)
```bash
python3 launcher.py
```
Escolha entre as 3 interfaces disponíveis.

### Opção 2: Interface Desktop
```bash
python3 smarttour_desktop.py
```
- **Design**: Tema escuro moderno com verde e dourado
- **Recursos**: KPIs em tempo real, upload de arquivos, progresso visual
- **Dependência**: `sudo apt install python3-tk`

### Opção 3: Interface Web  
```bash
python3 smarttour_web.py
```
- **Acesso**: http://localhost:5000
- **Design**: Interface web responsiva com tema ecológico
- **Recursos**: Upload drag-and-drop, análise em background, exportação

### Opção 4: Terminal (Análise Rápida)
```bash
python3 smarttour_integrated.py
```
- **Uso**: Análise direta com dados padrão
- **Saída**: Relatório HTML automático

## 📁 Estrutura Final (Refatorada)

```
hackathon-1/
├── 🎯 smarttour_integrated.py      # Sistema completo integrado
├── 🎯 main_simple.py              # Versão simplificada
├── 📊 Material_hackathon/         # Dados de exemplo
│   └── Data_set_examplos/
│       ├── Visitors_by_Province__preview_.csv
│       └── Eco_Sites__preview_.csv
├── 🔧 modules/                    # Módulos auxiliares
│   ├── __init__.py
│   ├── app_functions.py
│   └── app_settings.py
├── 📋 requirements.txt            # Dependências essenciais
└── 📖 README.md                   # Esta documentação
```

## 🎯 Funcionalidades Principais

### ✅ Sistema Integrado (`smarttour_integrated.py`)
- **Análise Completa**: Visitantes + Sítios Ecológicos
- **KPIs Automatizados**: Turismo, Sustentabilidade, Economia
- **Visualizações Interativas**: Gráficos Plotly
- **Relatório HTML**: Export automático
- **Log Sistema**: Rastreamento completo

### 📊 Análises Incluídas
- **Visitantes por Província**: Volume, sazonalidade, perfil
- **Sustentabilidade**: Índice de fragilidade, capacidade
- **KPIs Econômicos**: Receita estimada, taxas médias
- **Relatório Executivo**: Insights e recomendações

## 🔧 Dependências Essenciais

**Apenas 5 bibliotecas principais:**
- `pandas` - Manipulação de dados
- `numpy` - Computação numérica
- `matplotlib` - Visualizações básicas
- `seaborn` - Gráficos estatísticos  
- `plotly` - Dashboards interativos

## 📈 Exemplo de Saída

```
🇦🇴 SMARTTOUR ANGOLA - Sistema Integrado
============================================================
📊 Carregando dados...
✅ Dados carregados!
   • 4 províncias
   • 8 sítios ecológicos

🔍 Executando análise...
✅ Análise concluída!

📈 KPIs Principais:
   • Visitantes anuais: 2,380,848
   • Sites sustentáveis: 50.0%
   • Score sustentabilidade: 3.0/10

📄 Exportando relatório...
✅ Relatório exportado: smarttour_angola_report.html

🎉 SmartTour Angola executado com sucesso!
```

## 🎯 KPIs Principais

### 📊 Turismo
- **Visitantes Anuais**: Volume total estimado
- **% Estrangeiros**: Participação internacional
- **Estadia Média**: Duração das visitas
- **Variação Sazonal**: Época alta vs baixa

### 🌱 Sustentabilidade
- **% Sites Sustentáveis**: Sítios com baixa fragilidade
- **Score Médio**: Pontuação 0-10
- **Capacidade Total**: Visitantes/dia agregada
- **Cobertura**: Províncias atendidas

### 💰 Econômico
- **Receita Estimada**: Potencial anual (AOA)
- **Taxa Média**: Preço médio por sítio
- **Distribuição**: Equidade regional

## 🌍 Alinhamento com ODS

- **ODS 8**: Crescimento Econômico Sustentável
- **ODS 11**: Comunidades Sustentáveis
- **ODS 12**: Consumo Responsável
- **ODS 13**: Ação Climática
- **ODS 15**: Vida Terrestre

## 📄 Relatório HTML

O sistema gera automaticamente um relatório HTML completo com:

- 📊 **Dashboard Interativo**: KPIs visuais
- 📈 **Gráficos**: Visitantes por província
- 📋 **Tabelas**: Ranking de destinos
- 💡 **Recomendações**: Ações sugeridas
- 🎯 **Insights**: Principais achados

## 🔄 Uso Programático

```python
from smarttour_integrated import SmartTourAngola

# Criar instância
smarttour = SmartTourAngola()

# Carregar e analisar
smarttour.load_data()
smarttour.perform_analysis()

# Acessar resultados
kpis = smarttour.kpis
insights = smarttour.visitor_insights

# Exportar relatório
smarttour.export_report("meu_relatorio.html")
```
# 👥 Créditos

**Grupo 2 - FTL Bootcamp**
- 👑 **Team Leader**: Reinaldo Sambinga  
- 🎯 **Objetivo**: Sistema otimizado de turismo sustentável
- 🏆 **Resultado**: Refatoração completa e funcional

---

<div align="center">

**SmartTour Angola** 🇦🇴  
*"Sistema refatorado e otimizado para análise de turismo sustentável"*

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Data Science](https://img.shields.io/badge/Data-Science-green?logo=pandas)](https://pandas.pydata.org)
[![Visualization](https://img.shields.io/badge/Viz-Plotly-red?logo=plotly)](https://plotly.com)

**Sistema integrado e pronto para produção**

</div>
