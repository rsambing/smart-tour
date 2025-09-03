#!/usr/bin/env python3
"""
SmartTour Angola - Web App
Interface web moderna para análise de turismo sustentável
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file, flash
import os
import json
import threading
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
from pathlib import Path

# Import do sistema SmartTour
from smarttour_integrated import SmartTourAngola

app = Flask(__name__)
app.secret_key = 'smarttour_angola_2024_secretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Criar diretório de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Instância global do SmartTour
smarttour = SmartTourAngola()
analysis_status = {
    'running': False,
    'completed': False,
    'progress': 0,
    'message': 'Sistema pronto',
    'last_update': datetime.now().isoformat()
}

def allowed_file(filename):
    """Verifica se arquivo é permitido"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx', 'xls'}

@app.route('/')
def index():
    """Página inicial"""
    status = smarttour.get_status()
    return render_template('index.html', 
                         status=status, 
                         analysis_status=analysis_status)

@app.route('/load_default', methods=['POST'])
def load_default_data():
    """Carrega dados padrão"""
    try:
        success = smarttour.load_data()
        if success:
            analysis_status.update({
                'message': 'Dados padrão carregados com sucesso!',
                'last_update': datetime.now().isoformat()
            })
            flash('Dados padrão carregados com sucesso! ✅', 'success')
        else:
            flash('Erro ao carregar dados padrão ❌', 'error')
        
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_files():
    """Upload de arquivos personalizados"""
    try:
        visitors_file = request.files.get('visitors_file')
        eco_sites_file = request.files.get('eco_sites_file')
        
        if not visitors_file or not eco_sites_file:
            flash('Selecione ambos os arquivos (visitantes e sítios ecológicos)', 'warning')
            return redirect(url_for('index'))
        
        if not (allowed_file(visitors_file.filename) and allowed_file(eco_sites_file.filename)):
            flash('Formato de arquivo não permitido. Use CSV ou Excel.', 'error')
            return redirect(url_for('index'))
        
        # Salvar arquivos
        visitors_filename = secure_filename(visitors_file.filename)
        eco_sites_filename = secure_filename(eco_sites_file.filename)
        
        visitors_path = os.path.join(app.config['UPLOAD_FOLDER'], visitors_filename)
        eco_sites_path = os.path.join(app.config['UPLOAD_FOLDER'], eco_sites_filename)
        
        visitors_file.save(visitors_path)
        eco_sites_file.save(eco_sites_path)
        
        # Carregar dados
        success = smarttour.load_data(visitors_path, eco_sites_path)
        
        if success:
            analysis_status.update({
                'message': f'Dados personalizados carregados: {visitors_filename}, {eco_sites_filename}',
                'last_update': datetime.now().isoformat()
            })
            flash('Dados personalizados carregados com sucesso! ✅', 'success')
        else:
            flash('Erro ao carregar dados personalizados ❌', 'error')
        
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Erro no upload: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/analyze', methods=['POST'])
def run_analysis():
    """Executa análise em background"""
    if analysis_status['running']:
        flash('Análise já está em execução', 'warning')
        return redirect(url_for('index'))
    
    if not smarttour.data_loaded:
        flash('Carregue os dados primeiro!', 'warning')
        return redirect(url_for('index'))
    
    def analysis_task():
        analysis_status.update({
            'running': True,
            'completed': False,
            'progress': 10,
            'message': 'Iniciando análise...',
            'last_update': datetime.now().isoformat()
        })
        
        try:
            analysis_status.update({
                'progress': 30,
                'message': 'Processando dados de turismo...',
                'last_update': datetime.now().isoformat()
            })
            
            success = smarttour.perform_analysis()
            
            analysis_status.update({
                'progress': 80,
                'message': 'Finalizando análise...',
                'last_update': datetime.now().isoformat()
            })
            
            if success:
                analysis_status.update({
                    'running': False,
                    'completed': True,
                    'progress': 100,
                    'message': 'Análise concluída com sucesso!',
                    'last_update': datetime.now().isoformat()
                })
            else:
                analysis_status.update({
                    'running': False,
                    'completed': False,
                    'progress': 0,
                    'message': 'Erro na análise',
                    'last_update': datetime.now().isoformat()
                })
                
        except Exception as e:
            analysis_status.update({
                'running': False,
                'completed': False,
                'progress': 0,
                'message': f'Erro: {str(e)}',
                'last_update': datetime.now().isoformat()
            })
    
    # Executar análise em thread separada
    threading.Thread(target=analysis_task, daemon=True).start()
    
    flash('Análise iniciada! Acompanhe o progresso abaixo.', 'info')
    return redirect(url_for('index'))

@app.route('/api/status')
def get_status():
    """API para status atual"""
    status = smarttour.get_status()
    status.update(analysis_status)
    return jsonify(status)

@app.route('/api/kpis')
def get_kpis():
    """API para KPIs principais"""
    if not smarttour.analysis_completed:
        return jsonify({'error': 'Análise não concluída'})
    
    return jsonify(smarttour.kpis)

@app.route('/results')
def results():
    """Página de resultados"""
    if not smarttour.analysis_completed:
        flash('Execute a análise primeiro!', 'warning')
        return redirect(url_for('index'))
    
    return render_template('results.html', 
                         kpis=smarttour.kpis,
                         summary=smarttour.summary_report)

@app.route('/export_html')
def export_html():
    """Exporta relatório HTML"""
    if not smarttour.analysis_completed:
        flash('Execute a análise primeiro!', 'warning')
        return redirect(url_for('index'))
    
    try:
        filename = f"smarttour_angola_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        success = smarttour.export_report(filename)
        
        if success:
            flash(f'Relatório exportado: {filename}', 'success')
            return send_file(filename, as_attachment=True)
        else:
            flash('Erro ao exportar relatório', 'error')
            
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
    
    return redirect(url_for('results'))

# Template da página inicial
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇦🇴 SmartTour Angola</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #1a1a1a;
            --bg-medium: #2d2d2d;
            --bg-light: #404040;
            --green-primary: #00d084;
            --green-secondary: #66ff99;
            --gold: #ffd700;
            --gold-light: #ffed4e;
            --white: #ffffff;
            --gray: #cccccc;
            --red-angola: #CE1126;
            --yellow-angola: #FFCD00;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-dark);
            color: var(--white);
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, var(--red-angola), var(--yellow-angola));
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .card {
            background: var(--bg-medium);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border-left: 5px solid var(--green-primary);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: var(--gold);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .status-card {
            background: var(--bg-light);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .status-value {
            font-size: 2em;
            font-weight: bold;
            color: var(--green-primary);
            margin-bottom: 5px;
        }
        
        .btn {
            background: var(--green-primary);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            margin: 5px;
        }
        
        .btn:hover {
            background: var(--green-secondary);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-gold {
            background: var(--gold);
            color: var(--bg-dark);
        }
        
        .btn-gold:hover {
            background: var(--gold-light);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .progress-container {
            background: var(--bg-light);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .progress-bar {
            background: var(--bg-medium);
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, var(--green-primary), var(--green-secondary));
            height: 100%;
            transition: width 0.3s ease;
            border-radius: 10px;
        }
        
        .upload-area {
            border: 2px dashed var(--green-primary);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            background: var(--bg-light);
        }
        
        .file-input {
            margin: 10px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid var(--gray);
            background: var(--bg-medium);
            color: var(--white);
        }
        
        .alert {
            padding: 15px;
            margin: 15px 0;
            border-radius: 10px;
            border-left: 5px solid;
        }
        
        .alert-success {
            background: rgba(0, 208, 132, 0.1);
            border-color: var(--green-primary);
            color: var(--green-secondary);
        }
        
        .alert-error {
            background: rgba(206, 17, 38, 0.1);
            border-color: var(--red-angola);
            color: #ff6b6b;
        }
        
        .alert-warning {
            background: rgba(255, 205, 0, 0.1);
            border-color: var(--yellow-angola);
            color: var(--gold);
        }
        
        .alert-info {
            background: rgba(0, 208, 132, 0.1);
            border-color: var(--green-primary);
            color: var(--green-secondary);
        }
        
        #status-message {
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .rotating {
            animation: rotate 2s linear infinite;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-globe-africa"></i> SmartTour Angola</h1>
            <p>Sistema de Análise de Turismo Sustentável</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Descentralização e Ecoturismo | FTL Bootcamp</p>
        </div>
        
        <!-- Mensagens Flash -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        <i class="fas fa-{% if category == 'success' %}check-circle{% elif category == 'error' %}exclamation-circle{% elif category == 'warning' %}exclamation-triangle{% else %}info-circle{% endif %}"></i>
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <!-- Status Cards -->
        <div class="status-grid">
            <div class="status-card">
                <div class="status-value">{{ status.visitor_records }}</div>
                <div>Registros de Visitantes</div>
            </div>
            <div class="status-card">
                <div class="status-value">{{ status.provinces_available }}</div>
                <div>Províncias Disponíveis</div>
            </div>
            <div class="status-card">
                <div class="status-value">{{ status.eco_sites_available }}</div>
                <div>Sítios Ecológicos</div>
            </div>
            <div class="status-card">
                <div class="status-value" style="color: {% if status.data_loaded %}var(--green-primary){% else %}var(--red-angola){% endif %}">
                    {% if status.data_loaded %}✅{% else %}❌{% endif %}
                </div>
                <div>Dados Carregados</div>
            </div>
        </div>
        
        <!-- Controles de Dados -->
        <div class="card">
            <h3><i class="fas fa-database"></i> Carregamento de Dados</h3>
            
            <form method="POST" action="{{ url_for('load_default_data') }}" style="display: inline;">
                <button type="submit" class="btn" {% if analysis_status.running %}disabled{% endif %}>
                    <i class="fas fa-download"></i> Carregar Dados Padrão
                </button>
            </form>
            
            <div class="upload-area">
                <h4><i class="fas fa-cloud-upload-alt"></i> Upload de Dados Personalizados</h4>
                <form method="POST" action="{{ url_for('upload_files') }}" enctype="multipart/form-data">
                    <div>
                        <label for="visitors_file">Arquivo de Visitantes (CSV):</label>
                        <input type="file" name="visitors_file" id="visitors_file" class="file-input" accept=".csv,.xlsx,.xls" required>
                    </div>
                    <div>
                        <label for="eco_sites_file">Arquivo de Sítios Ecológicos (CSV):</label>
                        <input type="file" name="eco_sites_file" id="eco_sites_file" class="file-input" accept=".csv,.xlsx,.xls" required>
                    </div>
                    <button type="submit" class="btn" {% if analysis_status.running %}disabled{% endif %}>
                        <i class="fas fa-upload"></i> Carregar Arquivos
                    </button>
                </form>
            </div>
        </div>
        
        <!-- Controles de Análise -->
        <div class="card">
            <h3><i class="fas fa-chart-line"></i> Análise e Relatórios</h3>
            
            <form method="POST" action="{{ url_for('run_analysis') }}" style="display: inline;">
                <button type="submit" class="btn btn-gold" {% if not status.data_loaded or analysis_status.running %}disabled{% endif %}>
                    <i class="fas fa-play"></i> Executar Análise
                </button>
            </form>
            
            <a href="{{ url_for('results') }}" class="btn" {% if not status.analysis_completed %}style="opacity: 0.5; pointer-events: none;"{% endif %}>
                <i class="fas fa-chart-bar"></i> Ver Resultados
            </a>
            
            <a href="{{ url_for('export_html') }}" class="btn btn-gold" {% if not status.analysis_completed %}style="opacity: 0.5; pointer-events: none;"{% endif %}>
                <i class="fas fa-file-export"></i> Exportar Relatório
            </a>
        </div>
        
        <!-- Status da Análise -->
        <div class="progress-container" id="progress-container" {% if not analysis_status.running %}style="display: none;"{% endif %}>
            <div id="status-message">
                <i class="fas fa-cog rotating"></i> {{ analysis_status.message }}
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill" style="width: {{ analysis_status.progress }}%;"></div>
            </div>
            <div style="text-align: center; margin-top: 10px; font-size: 0.9em;">
                {{ analysis_status.progress }}% concluído
            </div>
        </div>
    </div>
    
    <script>
        // Atualizar status automaticamente
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const progressContainer = document.getElementById('progress-container');
                    const statusMessage = document.getElementById('status-message');
                    const progressFill = document.getElementById('progress-fill');
                    
                    if (data.running) {
                        progressContainer.style.display = 'block';
                        statusMessage.innerHTML = '<i class="fas fa-cog rotating"></i> ' + data.message;
                        progressFill.style.width = data.progress + '%';
                    } else if (data.completed) {
                        progressContainer.style.display = 'block';
                        statusMessage.innerHTML = '<i class="fas fa-check-circle"></i> ' + data.message;
                        progressFill.style.width = '100%';
                        setTimeout(() => {
                            location.reload();
                        }, 2000);
                    } else {
                        progressContainer.style.display = 'none';
                    }
                })
                .catch(error => console.error('Erro ao atualizar status:', error));
        }
        
        // Atualizar a cada 2 segundos se análise estiver rodando
        {% if analysis_status.running %}
        setInterval(updateStatus, 2000);
        {% endif %}
    </script>
</body>
</html>
"""

# Template da página de resultados
RESULTS_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Resultados - SmartTour Angola</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* Reutilizar estilos da página inicial */
        :root {
            --bg-dark: #1a1a1a;
            --bg-medium: #2d2d2d;
            --bg-light: #404040;
            --green-primary: #00d084;
            --green-secondary: #66ff99;
            --gold: #ffd700;
            --gold-light: #ffed4e;
            --white: #ffffff;
            --gray: #cccccc;
            --red-angola: #CE1126;
            --yellow-angola: #FFCD00;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-dark);
            color: var(--white);
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, var(--red-angola), var(--yellow-angola));
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .card {
            background: var(--bg-medium);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border-left: 5px solid var(--green-primary);
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .kpi-card {
            background: var(--bg-light);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .kpi-title {
            color: var(--gray);
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        
        .kpi-value {
            font-size: 2.2em;
            font-weight: bold;
            color: var(--green-primary);
        }
        
        .btn {
            background: var(--green-primary);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin: 5px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: var(--green-secondary);
            transform: translateY(-2px);
        }
        
        .btn-gold {
            background: var(--gold);
            color: var(--bg-dark);
        }
        
        .section-title {
            color: var(--gold);
            border-bottom: 2px solid var(--green-primary);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        .findings-list {
            list-style: none;
        }
        
        .findings-list li {
            background: var(--bg-light);
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid var(--green-primary);
        }
        
        .findings-list li:before {
            content: "💡 ";
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-chart-bar"></i> Resultados da Análise</h1>
            <p>SmartTour Angola - Insights de Turismo Sustentável</p>
        </div>
        
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 class="section-title" style="margin: 0;"><i class="fas fa-tachometer-alt"></i> KPIs Principais</h2>
                <div>
                    <a href="{{ url_for('index') }}" class="btn">
                        <i class="fas fa-arrow-left"></i> Voltar
                    </a>
                    <a href="{{ url_for('export_html') }}" class="btn btn-gold">
                        <i class="fas fa-download"></i> Exportar HTML
                    </a>
                </div>
            </div>
            
            <!-- KPIs de Turismo -->
            <h3 style="color: var(--green-secondary); margin: 20px 0 10px 0;">🎯 Turismo</h3>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Visitantes Anuais</div>
                    <div class="kpi-value">{{ "{:,}".format(kpis.tourism_kpis.total_annual_visitors) }}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Visitantes Estrangeiros</div>
                    <div class="kpi-value">{{ kpis.tourism_kpis.foreign_visitor_percentage }}%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Estadia Média</div>
                    <div class="kpi-value">{{ kpis.tourism_kpis.average_stay_duration }} noites</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Variação Sazonal</div>
                    <div class="kpi-value">{{ kpis.tourism_kpis.seasonal_variation }}%</div>
                </div>
            </div>
            
            <!-- KPIs de Sustentabilidade -->
            <h3 style="color: var(--green-secondary); margin: 20px 0 10px 0;">🌱 Sustentabilidade</h3>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Sites Sustentáveis</div>
                    <div class="kpi-value">{{ kpis.sustainability_kpis.sustainable_sites_percentage }}%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Capacidade Total</div>
                    <div class="kpi-value">{{ "{:,}".format(kpis.sustainability_kpis.total_eco_capacity) }}/dia</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Score Sustentabilidade</div>
                    <div class="kpi-value">{{ "%.1f"|format(kpis.sustainability_kpis.average_sustainability_score) }}/10</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Províncias Cobertas</div>
                    <div class="kpi-value">{{ kpis.sustainability_kpis.provinces_with_eco_sites }}</div>
                </div>
            </div>
            
            <!-- KPIs Econômicos -->
            <h3 style="color: var(--green-secondary); margin: 20px 0 10px 0;">💰 Econômico</h3>
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Receita Anual Estimada</div>
                    <div class="kpi-value" style="font-size: 1.8em;">{{ "{:,}".format(kpis.economic_kpis.estimated_annual_revenue) }} AOA</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Taxa Média por Sítio</div>
                    <div class="kpi-value" style="font-size: 1.8em;">{{ "{:,.0f}".format(kpis.economic_kpis.average_site_fee) }} AOA</div>
                </div>
            </div>
        </div>
        
        <!-- Principais Achados -->
        <div class="card">
            <h2 class="section-title"><i class="fas fa-lightbulb"></i> Principais Achados</h2>
            <ul class="findings-list">
                {% for finding in summary.executive_summary.key_findings %}
                <li>{{ finding }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <!-- Recomendações -->
        <div class="card">
            <h2 class="section-title"><i class="fas fa-bullseye"></i> Recomendações</h2>
            <ul class="findings-list">
                {% for recommendation in summary.executive_summary.recommendations %}
                <li style="border-left-color: var(--gold);">{{ recommendation }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <!-- Top Províncias -->
        <div class="card">
            <h2 class="section-title"><i class="fas fa-trophy"></i> Top Províncias por Visitantes</h2>
            {% for province, data in summary.top_provinces.items() %}
            <div style="background: var(--bg-light); margin: 10px 0; padding: 20px; border-radius: 10px;">
                <h4 style="color: var(--gold); margin-bottom: 10px;">{{ loop.index }}. {{ province }}</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                    <div>
                        <strong style="color: var(--green-secondary);">Visitantes:</strong><br>
                        {{ "{:,}".format(data.visitors) }}
                    </div>
                    <div>
                        <strong style="color: var(--green-secondary);">Estrangeiros:</strong><br>
                        {{ data.foreign_share }}%
                    </div>
                    <div>
                        <strong style="color: var(--green-secondary);">Estadia Média:</strong><br>
                        {{ "%.1f"|format(data.avg_stay) }} noites
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# Criar diretório de templates
os.makedirs('templates', exist_ok=True)

# Salvar templates
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(INDEX_TEMPLATE)

with open('templates/results.html', 'w', encoding='utf-8') as f:
    f.write(RESULTS_TEMPLATE)

def main():
    """Função principal"""
    print("🇦🇴 SmartTour Angola - Web App")
    print("=" * 50)
    print("🌐 Iniciando servidor web...")
    print("📱 Interface moderna com tema escuro ecológico")
    print("🚀 Acesse: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

if __name__ == "__main__":
    main()
