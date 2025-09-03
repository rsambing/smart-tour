"""
SmartTour - Main Application Module
Módulo principal da aplicação SmartTour
"""

import sys
import os
from pathlib import Path
import pandas as pd
import logging

# Adiciona o diretório smarttour ao path
current_dir = Path(__file__).parent
smarttour_dir = current_dir / "smarttour"
sys.path.insert(0, str(smarttour_dir))

# Imports do SmartTour
from smarttour.models.tourism_model import TouristData, EcoSiteData, RouteOptimizer
from smarttour.utils.data_processor import DataProcessor, DataValidator
from smarttour.visualization.charts import TourismVisualizer

class SmartTourApp:
    """Classe principal da aplicação SmartTour"""
    
    def __init__(self):
        self.setup_logging()
        self.data_processor = DataProcessor()
        self.visualizer = TourismVisualizer()
        
        # Dados principais
        self.tourist_data = None
        self.eco_sites_data = None
        self.route_optimizer = None
        
        # Insights processados
        self.visitor_insights = {}
        self.eco_insights = {}
        self.kpis = {}
        self.summary_report = {}
        
        # Status da aplicação
        self.data_loaded = False
        self.analysis_completed = False
        
        self.logger.info("SmartTour App inicializada")
    
    def setup_logging(self):
        """Configura sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/smarttour.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('SmartTour')
    
    def load_sample_data(self):
        """Carrega dados de exemplo do hackathon"""
        try:
            # Caminhos dos arquivos de exemplo (corrigido para 'uploads')
            base_path = Path(__file__).parent / "uploads"

            visitors_file = base_path / "Visitors_by_Province__preview_.csv"
            eco_sites_file = base_path / "Eco_Sites__preview_.csv"

            self.logger.info("Carregando dados de exemplo...")

            # Carrega dados de visitantes
            if visitors_file.exists():
                visitor_df = self.data_processor.load_csv_data(str(visitors_file), 'visitors')
                if not visitor_df.empty:
                    self.tourist_data = TouristData()
                    self.tourist_data.data = visitor_df
                    self.tourist_data.provinces = list(visitor_df['province'].unique())
                    self.tourist_data.years_range = list(visitor_df['year'].unique())
                    self.logger.info(f"Dados de visitantes carregados: {len(visitor_df)} registros")
                else:
                    self.logger.warning("Arquivo de visitantes vazio ou com erro")

            # Carrega dados de sítios ecológicos
            if eco_sites_file.exists():
                eco_df = self.data_processor.load_csv_data(str(eco_sites_file), 'eco_sites')
                if not eco_df.empty:
                    self.eco_sites_data = EcoSiteData()
                    self.eco_sites_data.data = eco_df
                    self.eco_sites_data.sites_by_province = eco_df.groupby('province')['site_name'].apply(list).to_dict()
                    self.logger.info(f"Dados de sítios ecológicos carregados: {len(eco_df)} registros")
                else:
                    self.logger.warning("Arquivo de sítios ecológicos vazio ou com erro")

            # Inicializa otimizador de rotas
            if self.tourist_data and self.eco_sites_data:
                self.route_optimizer = RouteOptimizer(self.eco_sites_data, self.tourist_data)
                self.data_loaded = True
                self.logger.info("SmartTour: Todos os dados carregados com sucesso!")
            else:
                self.logger.error("Falha ao carregar todos os dados necessários")

        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {e}")
            self.data_loaded = False
    
    def perform_analysis(self):
        """Executa análise completa dos dados"""
        if not self.data_loaded:
            self.logger.error("Dados não carregados. Execute load_sample_data() primeiro.")
            return False
        
        try:
            self.logger.info("Iniciando análise completa...")
            
            # Processa dados de visitantes
            if self.tourist_data and not self.tourist_data.data.empty:
                self.visitor_insights = self.data_processor.process_visitor_data(self.tourist_data.data)
                self.logger.info("Análise de visitantes concluída")
            
            # Processa dados de sítios ecológicos
            if self.eco_sites_data and not self.eco_sites_data.data.empty:
                self.eco_insights = self.data_processor.process_eco_sites_data(self.eco_sites_data.data)
                self.logger.info("Análise de sítios ecológicos concluída")
            
            # Gera KPIs
            self.kpis = self.data_processor.generate_kpis(self.visitor_insights, self.eco_insights)
            self.logger.info("KPIs gerados")
            
            # Cria relatório resumo
            self.summary_report = self.data_processor.create_summary_report(
                self.visitor_insights, self.eco_insights, self.kpis
            )
            self.logger.info("Relatório executivo criado")
            
            self.analysis_completed = True
            self.logger.info("Análise completa finalizada com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro durante análise: {e}")
            return False
    
    def get_province_analysis(self, province_name: str) -> dict:
        """Retorna análise detalhada de uma província específica"""
        if not self.analysis_completed:
            return {'error': 'Análise não realizada'}
        
        try:
            analysis = {
                'province': province_name,
                'tourism_stats': {},
                'eco_sites': [],
                'recommended_route': {},
                'sustainability_score': 0
            }
            
            # Estatísticas de turismo
            if self.tourist_data:
                analysis['tourism_stats'] = self.tourist_data.get_province_stats(province_name)
            
            # Sítios ecológicos da província
            if self.eco_sites_data and province_name in self.eco_sites_data.sites_by_province:
                site_names = self.eco_sites_data.sites_by_province[province_name]
                for site_name in site_names:
                    site_info = self.eco_sites_data.get_site_info(site_name)
                    if site_info:
                        analysis['eco_sites'].append(site_info)
            
            # Rota recomendada
            if self.route_optimizer:
                route = self.route_optimizer.create_sustainable_route(province_name)
                analysis['recommended_route'] = route
                
                # Score de sustentabilidade
                if 'avg_fragility' in route:
                    analysis['sustainability_score'] = self.route_optimizer.calculate_sustainability_score(route)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Erro ao analisar província {province_name}: {e}")
            return {'error': f'Erro na análise: {str(e)}'}
    
    def generate_visualizations(self) -> dict:
        """Gera todas as visualizações da aplicação"""
        if not self.analysis_completed:
            return {'error': 'Análise não realizada'}
        
        try:
            visualizations = {}
            
            # Gráfico de visitantes por província
            visualizations['province_visitors'] = self.visualizer.create_province_visitors_chart(self.visitor_insights)
            
            # Análise sazonal
            visualizations['seasonal_analysis'] = self.visualizer.create_seasonal_analysis_chart(self.visitor_insights)
            
            # Dashboard de sustentabilidade
            visualizations['sustainability_dashboard'] = self.visualizer.create_sustainability_dashboard(self.eco_insights)
            
            # Análise de capacidade
            visualizations['capacity_analysis'] = self.visualizer.create_capacity_analysis_chart(self.eco_insights)
            
            # Dashboard de KPIs
            visualizations['kpi_dashboard'] = self.visualizer.create_kpi_dashboard(self.kpis)
            
            # Gráfico executivo
            visualizations['executive_chart'] = self.visualizer.generate_executive_chart(self.summary_report)
            
            # Gráfico resumo matplotlib
            visualizations['summary_matplotlib'] = self.visualizer.create_matplotlib_summary(self.kpis)
            
            self.logger.info("Visualizações geradas com sucesso")
            return visualizations
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar visualizações: {e}")
            return {'error': f'Erro na geração: {str(e)}'}
    
    def export_analysis_report(self, output_path: str = "smarttour_report.html"):
        """Exporta relatório completo em HTML"""
        if not self.analysis_completed:
            self.logger.error("Análise não realizada")
            return False
        
        try:
            # Gera visualizações
            viz = self.generate_visualizations()
            
            # Template HTML
            html_template = """
            <!DOCTYPE html>
            <html lang="pt">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>SmartTour Angola - Relatório de Análise</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    .header {
                        background: linear-gradient(135deg, #CE1126, #FFCD00);
                        color: white;
                        padding: 30px;
                        text-align: center;
                        margin-bottom: 30px;
                        border-radius: 10px;
                    }
                    .section {
                        background: white;
                        margin: 20px 0;
                        padding: 25px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }
                    .kpi-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 20px;
                        margin: 20px 0;
                    }
                    .kpi-card {
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 8px;
                        text-align: center;
                        border-left: 4px solid #CE1126;
                    }
                    .kpi-value {
                        font-size: 2em;
                        font-weight: bold;
                        color: #CE1126;
                    }
                    .kpi-label {
                        color: #666;
                        margin-top: 10px;
                    }
                    h1, h2, h3 {
                        color: #333;
                    }
                    .visualization {
                        margin: 20px 0;
                        text-align: center;
                    }
                    .footer {
                        text-align: center;
                        color: #666;
                        margin-top: 40px;
                        padding: 20px;
                        border-top: 1px solid #eee;
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>SmartTour Angola</h1>
                    <p>Relatório de Análise de Turismo Sustentável</p>
                    <p>Gerado em: {date}</p>
                </div>
                
                <div class="section">
                    <h2>Resumo Executivo</h2>
                    <div class="kpi-grid">
                        <div class="kpi-card">
                            <div class="kpi-value">{total_visitors:,}</div>
                            <div class="kpi-label">Visitantes Anuais</div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-value">{sustainable_percentage}%</div>
                            <div class="kpi-label">Sites Sustentáveis</div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-value">{total_capacity:,}</div>
                            <div class="kpi-label">Capacidade Diária</div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-value">{provinces_count}</div>
                            <div class="kpi-label">Províncias Analisadas</div>
                        </div>
                    </div>
                    
                    <h3>Principais Achados</h3>
                    <ul>
                        {key_findings}
                    </ul>
                    
                    <h3>Recomendações</h3>
                    <ul>
                        {recommendations}
                    </ul>
                </div>
                
                <div class="section">
                    <h2>Dashboard de KPIs</h2>
                    <div class="visualization">
                        {kpi_dashboard}
                    </div>
                </div>
                
                <div class="section">
                    <h2>Análise por Província</h2>
                    <div class="visualization">
                        {province_chart}
                    </div>
                </div>
                
                <div class="section">
                    <h2>Análise Sazonal</h2>
                    <div class="visualization">
                        {seasonal_chart}
                    </div>
                </div>
                
                <div class="section">
                    <h2>Sustentabilidade dos Sítios</h2>
                    <div class="visualization">
                        {sustainability_dashboard}
                    </div>
                </div>
                
                <div class="section">
                    <h2>Análise de Capacidade</h2>
                    <div class="visualization">
                        {capacity_chart}
                    </div>
                </div>
                
                <div class="section">
                    <h2>Relatório Executivo</h2>
                    <div class="visualization">
                        {executive_chart}
                    </div>
                </div>
                
                <div class="section">
                    <h2>Resumo Visual</h2>
                    <div class="visualization">
                        {summary_chart}
                    </div>
                </div>
                
                <div class="footer">
                    <p>SmartTour Angola - Sistema de Análise de Turismo Sustentável</p>
                    <p>Desenvolvido para o FTL Bootcamp Hackathon</p>
                </div>
            </body>
            </html>
            """
            
            from datetime import datetime
            
            # Prepara dados para o template
            template_data = {
                'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'total_visitors': self.kpis.get('tourism_kpis', {}).get('total_annual_visitors', 0),
                'sustainable_percentage': self.kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0),
                'total_capacity': self.kpis.get('sustainability_kpis', {}).get('total_eco_capacity', 0),
                'provinces_count': self.kpis.get('sustainability_kpis', {}).get('provinces_with_eco_sites', 0),
                'key_findings': '\n'.join([f'<li>{finding}</li>' for finding in 
                                         self.summary_report.get('executive_summary', {}).get('key_findings', [])]),
                'recommendations': '\n'.join([f'<li>{rec}</li>' for rec in 
                                            self.summary_report.get('executive_summary', {}).get('recommendations', [])]),
                'kpi_dashboard': viz.get('kpi_dashboard', ''),
                'province_chart': viz.get('province_visitors', ''),
                'seasonal_chart': viz.get('seasonal_analysis', ''),
                'sustainability_dashboard': viz.get('sustainability_dashboard', ''),
                'capacity_chart': viz.get('capacity_analysis', ''),
                'executive_chart': viz.get('executive_chart', ''),
                'summary_chart': viz.get('summary_matplotlib', '')
            }
            
            # Gera HTML final
            html_content = html_template.format(**template_data)
            
            # Salva arquivo
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Relatório exportado para: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar relatório: {e}")
            return False
    
    def get_status(self) -> dict:
        """Retorna status atual da aplicação"""
        return {
            'data_loaded': self.data_loaded,
            'analysis_completed': self.analysis_completed,
            'provinces_available': len(self.tourist_data.provinces) if self.tourist_data else 0,
            'eco_sites_available': len(self.eco_sites_data.data) if self.eco_sites_data and not self.eco_sites_data.data.empty else 0,
            'has_insights': bool(self.visitor_insights and self.eco_insights),
            'has_kpis': bool(self.kpis),
            'has_summary': bool(self.summary_report)
        }

# Instância global da aplicação
smarttour_app = SmartTourApp()
