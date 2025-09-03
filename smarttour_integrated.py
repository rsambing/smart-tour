#!/usr/bin/env python3
"""
SmartTour Angola - Sistema Integrado
Sistema completo de análise de turismo sustentável em um único arquivo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from pathlib import Path
import logging
import base64
from io import BytesIO

class SmartTourAngola:
    """Sistema completo de análise de turismo sustentável para Angola"""
    
    def __init__(self):
        self.setup_logging()
        self.data_loaded = False
        self.analysis_completed = False
        
        # Dados
        self.visitor_data = None
        self.eco_sites_data = None
        
        # Resultados
        self.visitor_insights = {}
        self.eco_insights = {}
        self.kpis = {}
        self.summary_report = {}
        
        # Configurações
        self.angola_colors = {
            'primary': '#CE1126',    # Vermelho da bandeira
            'secondary': '#000000',  # Preto da bandeira  
            'accent': '#FFCD00',     # Amarelo da bandeira
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'info': '#17a2b8'
        }
        
        self.logger.info("SmartTour Angola inicializado")
    
    def setup_logging(self):
        """Configura logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/smarttour.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SmartTour')
    
    def load_data(self, visitors_file=None, eco_sites_file=None):
        """Carrega dados de arquivos CSV"""
        base_path = Path("uploads/")
        
        # Arquivos padrão se não especificados
        visitors_file = visitors_file or base_path / "Visitors_by_Province__preview_.csv"
        eco_sites_file = eco_sites_file or base_path / "Eco_Sites__preview_.csv"
        
        try:
            # Carrega dados de visitantes
            if Path(visitors_file).exists():
                self.visitor_data = pd.read_csv(visitors_file)
                self.visitor_data['date'] = pd.to_datetime(self.visitor_data['date'])
                self.logger.info(f"Visitantes: {len(self.visitor_data)} registros")
            
            # Carrega dados de sítios ecológicos
            if Path(eco_sites_file).exists():
                self.eco_sites_data = pd.read_csv(eco_sites_file)
                self.logger.info(f"Sítios ecológicos: {len(self.eco_sites_data)} registros")
            
            self.data_loaded = True
            self.logger.info("Dados carregados com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {e}")
            return False
    
    def analyze_visitors(self):
        """Analisa dados de visitantes"""
        if self.visitor_data is None or self.visitor_data.empty:
            return {}
        
        insights = {
            'overview': {
                'total_records': len(self.visitor_data),
                'provinces_count': self.visitor_data['province'].nunique(),
                'total_visitors': int(self.visitor_data['visitors_total'].sum()),
                'date_range': {
                    'start': self.visitor_data['date'].min().strftime('%Y-%m-%d'),
                    'end': self.visitor_data['date'].max().strftime('%Y-%m-%d')
                }
            },
            'provinces': {},
            'seasonal_patterns': {}
        }
        
        # Análise por província
        for province in self.visitor_data['province'].unique():
            province_data = self.visitor_data[self.visitor_data['province'] == province]
            insights['provinces'][province] = {
                'total_visitors': int(province_data['visitors_total'].sum()),
                'avg_foreign_share': round(province_data['foreign_share'].mean(), 3),
                'avg_stay_nights': round(province_data['avg_stay_nights'].mean(), 2)
            }
        
        # Padrões sazonais
        seasonal_data = self.visitor_data.groupby('season').agg({
            'visitors_total': ['sum', 'mean'],
            'foreign_share': 'mean',
            'avg_stay_nights': 'mean'
        }).round(2)
        
        insights['seasonal_patterns'] = {
            'peak_season': {
                'total_visitors': int(seasonal_data.loc['peak', ('visitors_total', 'sum')]),
                'avg_foreign_share': float(seasonal_data.loc['peak', ('foreign_share', 'mean')])
            },
            'offpeak_season': {
                'total_visitors': int(seasonal_data.loc['offpeak', ('visitors_total', 'sum')]),
                'avg_foreign_share': float(seasonal_data.loc['offpeak', ('foreign_share', 'mean')])
            }
        }
        
        return insights
    
    def analyze_eco_sites(self):
        """Analisa dados de sítios ecológicos"""
        if self.eco_sites_data is None or self.eco_sites_data.empty:
            return {}
        
        insights = {
            'overview': {
                'total_sites': len(self.eco_sites_data),
                'provinces_covered': self.eco_sites_data['province'].nunique(),
                'total_daily_capacity': int(self.eco_sites_data['capacity_daily'].sum()),
                'avg_fragility_index': round(self.eco_sites_data['fragility_index'].mean(), 2)
            },
            'by_province': {},
            'sustainability_analysis': {}
        }
        
        # Análise por província
        for province in self.eco_sites_data['province'].unique():
            province_data = self.eco_sites_data[self.eco_sites_data['province'] == province]
            insights['by_province'][province] = {
                'sites_count': len(province_data),
                'total_capacity': int(province_data['capacity_daily'].sum()),
                'avg_fragility': round(province_data['fragility_index'].mean(), 2),
                'sites': province_data['site_name'].tolist()
            }
        
        # Análise de sustentabilidade
        insights['sustainability_analysis'] = {
            'high_sustainability': int(len(self.eco_sites_data[self.eco_sites_data['fragility_index'] <= 2])),
            'moderate_sustainability': int(len(self.eco_sites_data[self.eco_sites_data['fragility_index'] == 3])),
            'requires_care': int(len(self.eco_sites_data[self.eco_sites_data['fragility_index'] == 4])),
            'high_fragility': int(len(self.eco_sites_data[self.eco_sites_data['fragility_index'] >= 5]))
        }
        
        return insights
    
    def calculate_kpis(self):
        """Calcula KPIs principais"""
        tourism_kpis = {}
        sustainability_kpis = {}
        economic_kpis = {}
        
        # KPIs de Turismo
        if self.visitor_insights:
            overview = self.visitor_insights.get('overview', {})
            tourism_kpis = {
                'total_annual_visitors': overview.get('total_visitors', 0) * 12,  # Estimativa anual
                'provinces_count': overview.get('provinces_count', 0)
            }
            
            # Percentual médio de estrangeiros
            if 'provinces' in self.visitor_insights:
                foreign_shares = [p.get('avg_foreign_share', 0) for p in self.visitor_insights['provinces'].values()]
                stay_durations = [p.get('avg_stay_nights', 0) for p in self.visitor_insights['provinces'].values()]
                tourism_kpis.update({
                    'foreign_visitor_percentage': round(np.mean(foreign_shares) * 100, 1),
                    'average_stay_duration': round(np.mean(stay_durations), 1)
                })
            
            # Variação sazonal
            if 'seasonal_patterns' in self.visitor_insights:
                peak = self.visitor_insights['seasonal_patterns'].get('peak_season', {}).get('total_visitors', 0)
                offpeak = self.visitor_insights['seasonal_patterns'].get('offpeak_season', {}).get('total_visitors', 0)
                if offpeak > 0:
                    tourism_kpis['seasonal_variation'] = round((peak - offpeak) / offpeak * 100, 1)
        
        # KPIs de Sustentabilidade
        if self.eco_insights:
            eco_overview = self.eco_insights.get('overview', {})
            sustainability_kpis = {
                'total_eco_capacity': eco_overview.get('total_daily_capacity', 0),
                'provinces_with_eco_sites': eco_overview.get('provinces_covered', 0)
            }
            
            if 'sustainability_analysis' in self.eco_insights:
                sustain_analysis = self.eco_insights['sustainability_analysis']
                total_sites = eco_overview.get('total_sites', 1)
                sustainable_sites = (sustain_analysis.get('high_sustainability', 0) + 
                                   sustain_analysis.get('moderate_sustainability', 0))
                sustainability_kpis['sustainable_sites_percentage'] = round((sustainable_sites / total_sites) * 100, 1)
            
            # Score de sustentabilidade
            avg_fragility = eco_overview.get('avg_fragility_index', 3)
            sustainability_kpis['average_sustainability_score'] = round(10 - (avg_fragility * 2), 1)
        
        # KPIs Econômicos
        if 'by_province' in self.eco_insights:
            fees = []
            total_revenue = 0
            for province_info in self.eco_insights['by_province'].values():
                avg_fee = self.eco_sites_data[self.eco_sites_data['province'] == list(self.eco_insights['by_province'].keys())[0]]['fee_aoa'].mean()
                fees.append(avg_fee)
                total_revenue += province_info.get('total_capacity', 0) * avg_fee
            
            economic_kpis = {
                'average_site_fee': round(np.mean(fees) if fees else 0, 2),
                'estimated_annual_revenue': int(total_revenue * 365 * 0.7)  # 70% ocupação
            }
        
        return {
            'tourism_kpis': tourism_kpis,
            'sustainability_kpis': sustainability_kpis,
            'economic_kpis': economic_kpis
        }
    
    def perform_analysis(self):
        """Executa análise completa"""
        if not self.data_loaded:
            self.logger.error("Dados não carregados")
            return False
        
        try:
            self.logger.info("Iniciando análise...")
            
            # Analisa visitantes
            self.visitor_insights = self.analyze_visitors()
            
            # Analisa sítios ecológicos
            self.eco_insights = self.analyze_eco_sites()
            
            # Calcula KPIs
            self.kpis = self.calculate_kpis()
            
            # Cria relatório resumo
            self.create_summary_report()
            
            self.analysis_completed = True
            self.logger.info("Análise completa!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro na análise: {e}")
            return False
    
    def create_summary_report(self):
        """Cria relatório executivo"""
        self.summary_report = {
            'executive_summary': {
                'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_provinces_analyzed': self.kpis.get('sustainability_kpis', {}).get('provinces_with_eco_sites', 0),
                'key_findings': [
                    f"Total de {self.kpis.get('tourism_kpis', {}).get('total_annual_visitors', 0):,} visitantes anuais estimados",
                    f"{self.kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0)}% dos sítios são sustentáveis",
                    f"Capacidade diária total de {self.kpis.get('sustainability_kpis', {}).get('total_eco_capacity', 0):,} visitantes",
                    f"Score médio de sustentabilidade: {self.kpis.get('sustainability_kpis', {}).get('average_sustainability_score', 0):.1f}/10"
                ],
                'recommendations': [
                    "Promover sítios com alta sustentabilidade",
                    "Desenvolver infraestrutura em províncias com baixo turismo",
                    "Implementar monitoramento de capacidade de carga"
                ]
            },
            'top_provinces': {}
        }
        
        # Top províncias por visitantes
        if 'provinces' in self.visitor_insights:
            sorted_provinces = sorted(
                self.visitor_insights['provinces'].items(),
                key=lambda x: x[1].get('total_visitors', 0),
                reverse=True
            )[:5]
            
            self.summary_report['top_provinces'] = {
                name: {
                    'visitors': data.get('total_visitors', 0),
                    'foreign_share': round(data.get('avg_foreign_share', 0) * 100, 1),
                    'avg_stay': data.get('avg_stay_nights', 0)
                }
                for name, data in sorted_provinces
            }
    
    def create_visualizations(self):
        """Cria visualizações principais"""
        visualizations = {}
        
        try:
            # Gráfico de visitantes por província
            if 'provinces' in self.visitor_insights:
                provinces = list(self.visitor_insights['provinces'].keys())
                visitors = [data['total_visitors'] for data in self.visitor_insights['provinces'].values()]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=provinces,
                    y=visitors,
                    marker_color=self.angola_colors['primary'],
                    text=[f"{v:,}" for v in visitors],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    title='Visitantes por Província',
                    xaxis_title='Província',
                    yaxis_title='Número de Visitantes',
                    template='plotly_white'
                )
                
                visualizations['province_visitors'] = fig.to_html(include_plotlyjs='cdn')
            
            # Dashboard de KPIs
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Visitantes vs Capacidade', 'Score Sustentabilidade', 'Distribuição Sazonal', 'KPIs Econômicos'),
                specs=[[{'type': 'bar'}, {'type': 'indicator'}], [{'type': 'pie'}, {'type': 'bar'}]]
            )
            
            # Visitantes vs Capacidade
            tourism_kpis = self.kpis.get('tourism_kpis', {})
            sustainability_kpis = self.kpis.get('sustainability_kpis', {})
            
            fig.add_trace(go.Bar(
                x=['Visitantes Anuais', 'Capacidade Anual'],
                y=[tourism_kpis.get('total_annual_visitors', 0), 
                   sustainability_kpis.get('total_eco_capacity', 0) * 365],
                marker_color=[self.angola_colors['primary'], self.angola_colors['accent']]
            ), row=1, col=1)
            
            # Score de sustentabilidade
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=sustainability_kpis.get('average_sustainability_score', 0),
                title={'text': "Sustentabilidade"},
                gauge={'axis': {'range': [None, 10]}, 'bar': {'color': self.angola_colors['success']}}
            ), row=1, col=2)
            
            # Distribuição sazonal
            if 'seasonal_patterns' in self.visitor_insights:
                seasonal = self.visitor_insights['seasonal_patterns']
                fig.add_trace(go.Pie(
                    labels=['Época Alta', 'Época Baixa'],
                    values=[seasonal['peak_season']['total_visitors'], seasonal['offpeak_season']['total_visitors']],
                    marker_colors=[self.angola_colors['primary'], self.angola_colors['accent']]
                ), row=2, col=1)
            
            # KPIs econômicos
            economic_kpis = self.kpis.get('economic_kpis', {})
            fig.add_trace(go.Bar(
                x=['Receita (M AOA)', 'Taxa Média (K AOA)'],
                y=[economic_kpis.get('estimated_annual_revenue', 0) / 1000000,
                   economic_kpis.get('average_site_fee', 0) / 1000],
                marker_color=self.angola_colors['info']
            ), row=2, col=2)
            
            fig.update_layout(title='Dashboard SmartTour Angola', height=700, showlegend=False)
            visualizations['kpi_dashboard'] = fig.to_html(include_plotlyjs='cdn')
            
        except Exception as e:
            self.logger.error(f"Erro ao criar visualizações: {e}")
        
        return visualizations
    
    def get_status(self):
        """Retorna status detalhado do sistema"""
        status = {
            'data_loaded': getattr(self, 'data_loaded', False),
            'analysis_completed': getattr(self, 'analysis_completed', False),
            'provinces_available': 0,
            'eco_sites_available': 0,
            'visitor_records': 0,
            'last_analysis': None
        }
        
        try:
            if hasattr(self, 'visitor_data') and self.visitor_data is not None:
                status['visitor_records'] = len(self.visitor_data)
                if 'province' in self.visitor_data.columns:
                    status['provinces_available'] = self.visitor_data['province'].nunique()
        except Exception as e:
            self.logger.warning(f"Erro ao obter status dos visitantes: {e}")
        
        try:
            if hasattr(self, 'eco_sites_data') and self.eco_sites_data is not None:
                status['eco_sites_available'] = len(self.eco_sites_data)
        except Exception as e:
            self.logger.warning(f"Erro ao obter status dos sítios: {e}")
        
        return status
    
    def export_report(self, filename="smarttour_angola_report.html"):
        """Exporta relatório HTML completo"""
        if not self.analysis_completed:
            return False
        
        try:
            visualizations = self.create_visualizations()
            
            html_content = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartTour Angola - Relatório</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #CE1126, #FFCD00); color: white; 
                   padding: 30px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
        .section {{ background: white; margin: 20px 0; padding: 25px; border-radius: 10px; 
                   box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 20px; margin: 20px 0; }}
        .kpi-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .kpi-value {{ font-size: 2em; font-weight: bold; color: #CE1126; }}
        h1, h2 {{ color: #333; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🇦🇴 SmartTour Angola</h1>
        <p>Sistema de Análise de Turismo Sustentável</p>
        <p>Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    
    <div class="section">
        <h2>📊 Resumo Executivo</h2>
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-value">{self.kpis.get('tourism_kpis', {}).get('total_annual_visitors', 0):,}</div>
                <div>Visitantes Anuais</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{self.kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0)}%</div>
                <div>Sites Sustentáveis</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{self.kpis.get('sustainability_kpis', {}).get('total_eco_capacity', 0):,}</div>
                <div>Capacidade Diária</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{self.kpis.get('sustainability_kpis', {}).get('average_sustainability_score', 0):.1f}</div>
                <div>Score Sustentabilidade</div>
            </div>
        </div>
        
        <h3>🎯 Principais Achados:</h3>
        <ul>{"".join([f"<li>{finding}</li>" for finding in self.summary_report.get('executive_summary', {}).get('key_findings', [])])}</ul>
        
        <h3>💡 Recomendações:</h3>
        <ul>{"".join([f"<li>{rec}</li>" for rec in self.summary_report.get('executive_summary', {}).get('recommendations', [])])}</ul>
    </div>
    
    <div class="section">
        <h2>📈 Visualizações</h2>
        {visualizations.get('province_visitors', '')}
        {visualizations.get('kpi_dashboard', '')}
    </div>
    
    <div class="section">
        <h2>🏆 Top Províncias</h2>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background: #f8f9fa;">
                <th style="padding: 10px; border: 1px solid #ddd;">Província</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Visitantes</th>
                <th style="padding: 10px; border: 1px solid #ddd;">% Estrangeiros</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Estadia Média</th>
            </tr>
            {"".join([f'<tr><td style="padding: 10px; border: 1px solid #ddd;">{province}</td><td style="padding: 10px; border: 1px solid #ddd;">{data["visitors"]:,}</td><td style="padding: 10px; border: 1px solid #ddd;">{data["foreign_share"]}%</td><td style="padding: 10px; border: 1px solid #ddd;">{data["avg_stay"]:.1f}</td></tr>' for province, data in self.summary_report.get('top_provinces', {}).items()])}
        </table>
    </div>
    
    <div style="text-align: center; color: #666; margin-top: 40px;">
        <p>SmartTour Angola - Desenvolvido para FTL Bootcamp</p>
    </div>
</body>
</html>
            """
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Relatório exportado: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar relatório: {e}")
            return False
    
    def get_status(self):
        """Retorna status da aplicação"""
        return {
            'data_loaded': self.data_loaded,
            'analysis_completed': self.analysis_completed,
            'provinces_available': self.visitor_data['province'].nunique() if self.visitor_data is not None else 0,
            'eco_sites_available': len(self.eco_sites_data) if self.eco_sites_data is not None else 0
        }

def main():
    """Função principal de demonstração"""
    print("🇦🇴 SMARTTOUR ANGOLA - Sistema Integrado")
    print("=" * 60)
    
    # Cria instância
    smarttour = SmartTourAngola()
    
    # Carrega dados
    print("📊 Carregando dados...")
    if smarttour.load_data():
        print("✅ Dados carregados!")
        
        # Executa análise
        print("🔍 Executando análise...")
        if smarttour.perform_analysis():
            print("✅ Análise concluída!")
            
            # Mostra KPIs
            kpis = smarttour.kpis
            print("\n📈 KPIs Principais:")
            print(f"   • Visitantes anuais: {kpis.get('tourism_kpis', {}).get('total_annual_visitors', 0):,}")
            print(f"   • Sites sustentáveis: {kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0)}%")
            print(f"   • Score sustentabilidade: {kpis.get('sustainability_kpis', {}).get('average_sustainability_score', 0):.1f}/10")
            
            # Exporta relatório
            print("\n📄 Exportando relatório...")
            if smarttour.export_report():
                print("✅ Relatório exportado: smarttour_angola_report.html")
            
            print("\n🎉 SmartTour Angola executado com sucesso!")
            return True
    
    print("❌ Erro na execução")
    return False

if __name__ == "__main__":
    main()
