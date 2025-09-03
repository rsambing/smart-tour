A **estrutura do projeto**, dá pra conectar a descrição com o código e mostrar claramente onde cada parte entra. Vou te dar um **mapa explicativo da arquitetura**:

---

## 🗂️ Estrutura do Projeto SmartTour

```
smart-tour/
├── docs/                     # Documentação do projeto
│   ├── requirements.txt       # Dependências principais
│   └── SOLUCOES.md            # Soluções propostas / guia interno
│
├── logs/                     # Logs do sistema
│   └── smarttour.log
│
├── modules/                  # Funções auxiliares genéricas
│   ├── app_functions.py       # Funções de suporte para app principal
│   └── __init__.py
│
├── smarttour/                # Core da aplicação
│   ├── config.py              # Configurações globais (paths, constantes, etc.)
│   ├── models/                # Modelos de dados
│   │   └── tourism_model.py   # Modelo de análise turística/sustentabilidade
│   ├── utils/                 # Utilitários
│   │   └── data_processor.py  # Limpeza e processamento dos datasets (CSV)
│   └── visualization/         # Camada de visualização
│       └── charts.py          # Criação de gráficos (matplotlib/plotly)
│
├── templates/                # Templates HTML (modo web)
│   ├── index.html             # Página inicial (upload/inputs)
│   └── results.html           # Página de resultados/relatórios
│
├── uploads/                  # Arquivos de entrada (datasets)
│   ├── Eco_Sites__preview_.csv
│   └── Visitors_by_Province__preview_.csv
│
├── launcher.py               # Script de inicialização principal
├── smarttour_app.py          # Interface desktop (PySide6/Qt)
├── smarttour_web.py          # Interface web (Flask/FastAPI)
├── smarttour_integrated.py   # Versão integrada (provavelmente web + desktop)
├── smarttour_desktop_safe.py # Variante desktop estável/testada
├── smarttour_angola_report.html # Relatório gerado
├── test_smarttour.py         # Testes automatizados
├── README.md                 # Descrição do projeto
```

---

## 🔎 Onde mexer para mudar o **layout** e funcionalidades

1. **Frontend (layout e UI)**

   * **Desktop (PySide6/Qt):**
     Arquivo: `smarttour_app.py`
     → aqui é onde você pode mudar botões, janelas, ícones, cores, etc.

   * **Web (Flask + HTML):**
     Arquivos: `templates/index.html` e `templates/results.html`
     → aqui você altera o design da página web, botões, progresso, dashboards.

2. **Gráficos e visualização**

   * Arquivo: `smarttour/visualization/charts.py`
     → se quiser mudar como os gráficos aparecem (linha, barra, pizza, etc).

3. **Processamento de dados**

   * Arquivo: `smarttour/utils/data_processor.py`
     → responsável por ler e limpar os CSV (`uploads/`).
     Aqui você edita se quiser novas métricas ou colunas.

4. **Modelos (pontuação de sustentabilidade, KPIs)**

   * Arquivo: `smarttour/models/tourism_model.py`
     → define como calcular índices de fragilidade, capacidade, score etc.

5. **Configurações globais**

   * Arquivo: `smarttour/config.py`
     → caminhos, constantes, opções padrão do sistema.

---

👉 Em resumo:

* **Quer mudar a cara?** → `smarttour_app.py` (desktop) e `templates/` (web).
* **Quer mudar como calcula?** → `tourism_model.py` (lógica) e `data_processor.py` (dados).
* **Quer mudar gráficos?** → `charts.py`.

---
