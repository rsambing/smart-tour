#!/usr/bin/env python3
"""
SmartTour Angola - Sistema Unificado de Análise de Turismo
Sistema centralizado que elimina redundâncias e simplifica o código
Autor: Sistema de IA - Versão Simplificada
Data: 2024
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import logging
from datetime import datetime
from types import SimpleNamespace

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from pathlib import Path
import logging
import os

class SmartTourCore:
    """
    Núcleo simplificado do SmartTour Angola
    Centraliza toda a lógica de análise em um local
    """
    
    def __init__(self):
        self.setup_logging()
        
        # Status do sistema
        self.data_loaded = False
        self.analysis_completed = False
        
        # Dados principais
        self.visitors_df = None
        self.sites_df = None
        
        # Resultados da análise
        self.visitor_stats = {}
        self.site_stats = {}
        self.kpis = {}
        # Removido self.summary_report dict para evitar conflito com método
        
        # Cores do tema de Angola
        self.colors = {
            'vermelho': '#CE1126',
            'amarelo': '#FFCD00', 
            'preto': '#000000',
            'verde': '#28a745'
        }
        
        self.logger.info("SmartTour Core inicializado")
    
    def setup_logging(self):
        """Configura sistema de log"""
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/smarttour.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SmartTour')
    
    def load_data(self, visitors_file=None, sites_file=None):
        """
        Carrega dados dos arquivos CSV
        Se não especificado, usa arquivos padrão da pasta uploads/
        """
        try:
            # Define arquivos padrão se não especificados
            base_path = Path("uploads")
            visitors_file = visitors_file or base_path / "Visitors_by_Province__preview_.csv"
            sites_file = sites_file or base_path / "Eco_Sites__preview_.csv"
            
            # Carrega dados de visitantes
            if Path(visitors_file).exists():
                self.visitors_df = pd.read_csv(visitors_file)
                self.visitors_df['date'] = pd.to_datetime(self.visitors_df['date'])
                self.logger.info(f"Visitantes carregados: {len(self.visitors_df)} registros")
            else:
                self.logger.error(f"Arquivo não encontrado: {visitors_file}")
                return False
            
            # Carrega dados de sítios ecológicos
            if Path(sites_file).exists():
                self.sites_df = pd.read_csv(sites_file)
                self.logger.info(f"Sítios carregados: {len(self.sites_df)} registros")
            else:
                self.logger.error(f"Arquivo não encontrado: {sites_file}")
                return False
            
            self.data_loaded = True
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {e}")
            return False
    
    def analyze_visitors(self):
        """Analisa dados de visitantes"""
        if self.visitors_df is None or self.visitors_df.empty:
            return {}
        
        # Estatísticas básicas
        total_visitors = int(self.visitors_df['visitors_total'].sum())
        provinces_count = self.visitors_df['province'].nunique()
        
        # Análise por província
        province_stats = {}
        for province in self.visitors_df['province'].unique():
            prov_data = self.visitors_df[self.visitors_df['province'] == province]
            province_stats[province] = {
                'total_visitors': int(prov_data['visitors_total'].sum()),
                'foreign_percentage': round(prov_data['foreign_share'].mean() * 100, 1),
                'avg_stay_nights': round(prov_data['avg_stay_nights'].mean(), 1)
            }
        
        # Análise sazonal
        seasonal_data = self.visitors_df.groupby('season')['visitors_total'].sum()
        
        self.visitor_stats = {
            'total_visitors': total_visitors,
            'provinces_count': provinces_count,
            'by_province': province_stats,
            'seasonal': {
                'peak_visitors': int(seasonal_data.get('peak', 0)),
                'offpeak_visitors': int(seasonal_data.get('offpeak', 0))
            }
        }
        
        return self.visitor_stats
    
    def analyze_sites(self):
        """Analisa dados de sítios ecológicos"""
        if self.sites_df is None or self.sites_df.empty:
            return {}
        
        # Estatísticas básicas
        total_sites = len(self.sites_df)
        total_capacity = int(self.sites_df['capacity_daily'].sum())
        avg_fragility = round(self.sites_df['fragility_index'].mean(), 2)
        
        # Análise de sustentabilidade
        high_sustain = len(self.sites_df[self.sites_df['fragility_index'] <= 2])
        moderate_sustain = len(self.sites_df[self.sites_df['fragility_index'] == 3])
        low_sustain = len(self.sites_df[self.sites_df['fragility_index'] >= 4])
        
        sustainable_percentage = round((high_sustain + moderate_sustain) / total_sites * 100, 1)
        
        # Análise por província
        province_sites = {}
        for province in self.sites_df['province'].unique():
            prov_data = self.sites_df[self.sites_df['province'] == province]
            province_sites[province] = {
                'sites_count': len(prov_data),
                'capacity': int(prov_data['capacity_daily'].sum()),
                'avg_fragility': round(prov_data['fragility_index'].mean(), 2),
                'sites_list': prov_data['site_name'].tolist()
            }
        
        self.site_stats = {
            'total_sites': total_sites,
            'total_capacity': total_capacity,
            'avg_fragility': avg_fragility,
            'sustainable_percentage': sustainable_percentage,
            'sustainability_breakdown': {
                'high_sustain': high_sustain,
                'moderate_sustain': moderate_sustain,
                'low_sustain': low_sustain
            },
            'by_province': province_sites
        }
        
        return self.site_stats
    
    def calculate_kpis(self):
        """Calcula KPIs principais do sistema"""
        if not self.visitor_stats or not self.site_stats:
            return {}
        
        # KPIs de turismo (estimativa anual baseada nos dados mensais)
        monthly_visitors = self.visitor_stats['total_visitors']
        annual_visitors = monthly_visitors * 12
        
        # KPIs de sustentabilidade
        sustainability_score = round(10 - (self.site_stats['avg_fragility'] * 2), 1)
        
        # KPIs econômicos (estimativa básica)
        avg_fee = self.sites_df['fee_aoa'].mean() if 'fee_aoa' in self.sites_df.columns else 5000
        estimated_revenue = int(self.site_stats['total_capacity'] * avg_fee * 365 * 0.6)  # 60% ocupação
        
        # Calcula percentuais médios
        avg_foreign_percentage = round(np.mean([p['foreign_percentage'] for p in self.visitor_stats['by_province'].values()]), 1)
        avg_stay_duration = round(np.mean([p['avg_stay_nights'] for p in self.visitor_stats['by_province'].values()]), 1)
        
        # Calcula variação sazonal
        seasonal_variation = 0
        if self.visitor_stats['seasonal']['peak_visitors'] > 0 and self.visitor_stats['seasonal']['offpeak_visitors'] > 0:
            peak = self.visitor_stats['seasonal']['peak_visitors']
            offpeak = self.visitor_stats['seasonal']['offpeak_visitors']
            seasonal_variation = round((peak - offpeak) / offpeak * 100, 1)
        
        # Estrutura compatível com template web (usando SimpleNamespace para acesso por atributo)
        from types import SimpleNamespace
        
        self.kpis = SimpleNamespace(
            tourism_kpis=SimpleNamespace(
                total_annual_visitors=annual_visitors,
                provinces_count=self.visitor_stats['provinces_count'],
                foreign_visitor_percentage=avg_foreign_percentage,
                average_stay_duration=avg_stay_duration,
                seasonal_variation=seasonal_variation
            ),
            sustainability_kpis=SimpleNamespace(
                total_sites=self.site_stats['total_sites'],
                total_eco_capacity=self.site_stats['total_capacity'],
                sustainable_sites_percentage=self.site_stats['sustainable_percentage'],
                average_sustainability_score=sustainability_score,
                provinces_with_eco_sites=len(self.site_stats['by_province'])
            ),
            economic_kpis=SimpleNamespace(
                estimated_annual_revenue=estimated_revenue,
                average_site_fee=round(avg_fee, 0)
            )
        )
        
        # Também mantém estrutura em dict para compatibilidade com outras interfaces
        self.kpis_dict = {
            'tourism': {
                'annual_visitors': annual_visitors,
                'provinces_count': self.visitor_stats['provinces_count'],
                'avg_foreign_percentage': avg_foreign_percentage
            },
            'sustainability': {
                'total_sites': self.site_stats['total_sites'],
                'total_capacity': self.site_stats['total_capacity'],
                'sustainable_percentage': self.site_stats['sustainable_percentage'],
                'sustainability_score': sustainability_score
            },
            'economic': {
                'estimated_annual_revenue': estimated_revenue,
                'avg_site_fee': round(avg_fee, 0)
            }
        }
        
        return self.kpis
    
    def summary_report(self):
        """Gera relatório resumido para apresentação"""
        if not hasattr(self, 'kpis'):
            self.calculate_kpis()
        
        # Para uso no terminal (string simples)
        if hasattr(self, '_terminal_format'):
            summary = []
            tourism = self.kpis.tourism_kpis
            summary.append(f"🏛️ TURISMO: {tourism.total_annual_visitors:,} visitantes/ano em {tourism.provinces_count} províncias")
            summary.append(f"   • {tourism.foreign_visitor_percentage}% visitantes estrangeiros")
            summary.append(f"   • Estadia média: {tourism.average_stay_duration} noites")
            
            sust = self.kpis.sustainability_kpis
            summary.append(f"🌱 SUSTENTABILIDADE: {sust.total_sites} sítios ecoturísticos")
            summary.append(f"   • {sust.sustainable_sites_percentage}% dos sítios são sustentáveis")
            summary.append(f"   • Score médio: {sust.average_sustainability_score}/10")
            
            econ = self.kpis.economic_kpis
            summary.append(f"💰 ECONOMIA: {econ.estimated_annual_revenue:,} AOA/ano estimado")
            summary.append(f"   • Taxa média: {econ.average_site_fee:,} AOA")
            
            return "\n".join(summary)
        
        # Para uso no template web (estrutura complexa)
        from types import SimpleNamespace
        
        summary = SimpleNamespace()
        summary.executive_summary = SimpleNamespace()
        
        # Principais achados baseados nos dados
        tourism = self.kpis.tourism_kpis
        sust = self.kpis.sustainability_kpis
        econ = self.kpis.economic_kpis
        
        summary.executive_summary.key_findings = [
            f"Angola recebe aproximadamente {tourism.total_annual_visitors:,} visitantes por ano",
            f"{tourism.foreign_visitor_percentage}% dos visitantes são estrangeiros",
            f"Tempo médio de estadia é de {tourism.average_stay_duration} noites",
            f"Existem {sust.total_sites} sítios ecoturísticos mapeados",
            f"{sust.sustainable_sites_percentage}% dos sítios seguem práticas sustentáveis",
            f"Receita estimada do ecoturismo: {econ.estimated_annual_revenue:,} AOA/ano"
        ]
        
        # Top províncias (simulado com dados reais se disponível)
        summary.top_provinces = {}
        if hasattr(self, 'visitor_stats') and 'by_province' in self.visitor_stats:
            # Usar dados reais se disponível
            sorted_provinces = sorted(
                self.visitor_stats['by_province'].items(),
                key=lambda x: x[1].get('total_visitors', 0),
                reverse=True
            )[:5]
            
            for name, data in sorted_provinces:
                summary.top_provinces[name] = {
                    'visitors': data.get('total_visitors', 0),
                    'foreign_share': data.get('foreign_percentage', 0),
                    'avg_stay': data.get('avg_stay_nights', 0)
                }
        else:
            # Dados de exemplo se não houver dados reais
            summary.top_provinces = {
                'Luanda': {'visitors': 850000, 'foreign_share': 45.2, 'avg_stay': 3.5},
                'Benguela': {'visitors': 320000, 'foreign_share': 28.7, 'avg_stay': 4.1},
                'Huíla': {'visitors': 280000, 'foreign_share': 35.1, 'avg_stay': 5.2},
                'Namibe': {'visitors': 190000, 'foreign_share': 52.3, 'avg_stay': 6.8},
                'Cabinda': {'visitors': 150000, 'foreign_share': 41.9, 'avg_stay': 3.9}
            }
        
        return summary
    
    def get_terminal_summary(self):
        """Retorna resumo em formato string para terminal"""
        if not hasattr(self, 'kpis'):
            self.calculate_kpis()
            
        summary = []
        tourism = self.kpis.tourism_kpis
        summary.append(f"🏛️ TURISMO: {tourism.total_annual_visitors:,} visitantes/ano em {tourism.provinces_count} províncias")
        summary.append(f"   • {tourism.foreign_visitor_percentage}% visitantes estrangeiros")
        summary.append(f"   • Estadia média: {tourism.average_stay_duration} noites")
        
        sust = self.kpis.sustainability_kpis
        summary.append(f"🌱 SUSTENTABILIDADE: {sust.total_sites} sítios ecoturísticos")
        summary.append(f"   • {sust.sustainable_sites_percentage}% dos sítios são sustentáveis")
        summary.append(f"   • Score médio: {sust.average_sustainability_score}/10")
        
        econ = self.kpis.economic_kpis
        summary.append(f"💰 ECONOMIA: {econ.estimated_annual_revenue:,} AOA/ano estimado")
        summary.append(f"   • Taxa média: {econ.average_site_fee:,} AOA")
        
        return "\n".join(summary)
    
    def perform_analysis(self):
        """Executa análise completa dos dados"""
        if not self.data_loaded:
            self.logger.error("Carregue os dados primeiro")
            return False
        
        try:
            self.logger.info("Iniciando análise...")
            
            # Executa análises
            self.analyze_visitors()
            self.analyze_sites()
            self.calculate_kpis()
            
            self.analysis_completed = True
            self.logger.info("Análise concluída com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro na análise: {e}")
            return False
    
    def create_charts(self):
        """Cria gráficos principais"""
        if not self.analysis_completed:
            return {}
        
        charts = {}
        
        try:
            # Gráfico de visitantes por província
            if self.visitor_stats['by_province']:
                provinces = list(self.visitor_stats['by_province'].keys())
                visitors = [data['total_visitors'] for data in self.visitor_stats['by_province'].values()]
                
                fig = px.bar(
                    x=provinces, y=visitors,
                    title="Visitantes por Província",
                    color_discrete_sequence=[self.colors['vermelho']]
                )
                fig.update_layout(
                    xaxis_title="Província",
                    yaxis_title="Número de Visitantes"
                )
                charts['visitors_by_province'] = fig.to_html(include_plotlyjs='cdn')
            
            # Dashboard de KPIs
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Visitantes Anuais', 'Score Sustentabilidade', 'Receita Anual (M AOA)', 'Capacidade Eco'),
                specs=[[{'type': 'bar'}, {'type': 'indicator'}],
                       [{'type': 'bar'}, {'type': 'indicator'}]]
            )
            
            # Usar self.kpis_dict para compatibilidade
            fig.add_trace(go.Bar(
                x=['Visitantes'],
                y=[self.kpis_dict['tourism']['annual_visitors']], 
                name='Visitantes',
                marker_color=self.colors['vermelho']
            ), row=1, col=1)
            
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=self.kpis_dict['sustainability']['sustainability_score'],
                title={'text': "Score"},
                gauge={'axis': {'range': [None, 10]},
                       'bar': {'color': self.colors['verde']},
                       'steps': [{'range': [0, 5], 'color': "lightgray"},
                                {'range': [5, 8], 'color': "yellow"},
                                {'range': [8, 10], 'color': "green"}]}
            ), row=1, col=2)
            
            revenue_millions = self.kpis_dict['economic']['estimated_annual_revenue'] / 1_000_000
            
            fig.update_layout(title="Dashboard SmartTour Angola", height=600, showlegend=False)
            charts['kpi_dashboard'] = fig.to_html(include_plotlyjs='cdn')
            
        except Exception as e:
            self.logger.error(f"Erro ao criar gráficos: {e}")
        
        return charts
    
    def export_report(self, filename="smarttour_angola_report.html"):
        """Exporta relatório HTML completo"""
        if not self.analysis_completed:
            self.logger.error("Execute a análise primeiro")
            return False
        
        try:
            charts = self.create_charts()
            
            # Template HTML simplificado
            html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>SmartTour Angola - Relatório</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #CE1126, #FFCD00); 
                   color: white; padding: 30px; text-align: center; 
                   border-radius: 10px; margin-bottom: 20px; }}
        .section {{ background: white; margin: 20px 0; padding: 25px; 
                    border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); 
                     gap: 20px; margin: 20px 0; }}
        .kpi-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; 
                     text-align: center; border-left: 4px solid #CE1126; }}
        .kpi-value {{ font-size: 2em; font-weight: bold; color: #CE1126; }}
        .kpi-label {{ color: #666; margin-top: 10px; }}
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
                <div class="kpi-value">{self.kpis_dict['tourism']['annual_visitors']:,}</div>
                <div class="kpi-label">Visitantes Anuais</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{self.kpis_dict['sustainability']['sustainable_percentage']}%</div>
                <div class="kpi-label">Sites Sustentáveis</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{self.kpis_dict['sustainability']['total_capacity']:,}</div>
                <div class="kpi-label">Capacidade Diária</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{self.kpis_dict['sustainability']['sustainability_score']}</div>
                <div class="kpi-label">Score Sustentabilidade</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>📈 Visualizações</h2>
        {charts.get('visitors_by_province', '')}
        {charts.get('kpi_dashboard', '')}
    </div>
    
    <div class="section">
        <h2>🏆 Top Províncias por Visitantes</h2>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background: #f8f9fa;">
                <th style="padding: 10px; border: 1px solid #ddd;">Província</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Visitantes</th>
                <th style="padding: 10px; border: 1px solid #ddd;">% Estrangeiros</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Estadia Média (noites)</th>
            </tr>"""
            
            # Ordena províncias por visitantes
            sorted_provinces = sorted(
                self.visitor_stats['by_province'].items(),
                key=lambda x: x[1]['total_visitors'],
                reverse=True
            )
            
            for province, data in sorted_provinces:
                html += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{province}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{data['total_visitors']:,}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{data['foreign_percentage']}%</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{data['avg_stay_nights']}</td>
            </tr>"""
            
            html += """
        </table>
    </div>
    
    <div style="text-align: center; color: #666; margin-top: 40px; padding: 20px;">
        <p>SmartTour Angola - Sistema de Análise de Turismo Sustentável</p>
        <p>Desenvolvido para o FTL Bootcamp Hackathon</p>
    </div>
</body>
</html>"""
            
            # Salva o arquivo
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            
            self.logger.info(f"Relatório exportado: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar relatório: {e}")
            return False
    
    def get_status(self):
        """Retorna status atual do sistema (compatível com interfaces)"""
        return {
            'data_loaded': self.data_loaded,
            'analysis_completed': self.analysis_completed,
            'visitor_records': len(self.visitors_df) if self.visitors_df is not None else 0,
            'eco_sites_available': len(self.sites_df) if self.sites_df is not None else 0,
            'provinces_available': self.visitors_df['province'].nunique() if self.visitors_df is not None else 0
        }


# Instância global para compatibilidade com código existente
smarttour_core = SmartTourCore()

# Classe compatível com o sistema antigo
class SmartTourAngola(SmartTourCore):
    """Classe de compatibilidade com o sistema antigo"""
    pass
