"""
SmartTour - Visualization Module
Geração de visualizações e gráficos para análise turística
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import base64
from io import BytesIO

class TourismVisualizer:
    """Classe para criação de visualizações do SmartTour"""
    
    def __init__(self):
        # Configuração de estilo
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # Cores personalizadas para Angola
        self.angola_colors = {
            'primary': '#CE1126',    # Vermelho da bandeira
            'secondary': '#000000',   # Preto da bandeira
            'accent': '#FFCD00',     # Amarelo da bandeira
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'info': '#17a2b8'
        }
    
    def create_province_visitors_chart(self, visitor_data: Dict) -> str:
        """Cria gráfico de visitantes por província"""
        if 'provinces' not in visitor_data:
            return ""
        
        try:
            # Prepara os dados
            provinces = list(visitor_data['provinces'].keys())
            visitors = [data['total_visitors'] for data in visitor_data['provinces'].values()]
            
            # Cria o gráfico
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=provinces,
                y=visitors,
                marker_color=self.angola_colors['primary'],
                text=[f"{v:,}" for v in visitors],
                textposition='outside'
            ))
            
            fig.update_layout(
                title={
                    'text': 'Visitantes por Província',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': self.angola_colors['secondary']}
                },
                xaxis_title='Província',
                yaxis_title='Número de Visitantes',
                template='plotly_white',
                height=500,
                showlegend=False,
                xaxis=dict(tickangle=45)
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id="province_visitors_chart")
            
        except Exception as e:
            print(f"Erro ao criar gráfico de províncias: {e}")
            return ""
    
    def create_seasonal_analysis_chart(self, visitor_data: Dict) -> str:
        """Cria gráfico de análise sazonal"""
        if 'seasonal_patterns' not in visitor_data:
            return ""
        
        try:
            seasonal = visitor_data['seasonal_patterns']
            
            seasons = ['Época Alta', 'Época Baixa']
            visitors = [
                seasonal['peak_season']['total_visitors'],
                seasonal['offpeak_season']['total_visitors']
            ]
            
            fig = go.Figure()
            
            fig.add_trace(go.Pie(
                labels=seasons,
                values=visitors,
                marker_colors=[self.angola_colors['primary'], self.angola_colors['accent']],
                hole=0.4,
                textinfo='label+percent+value',
                textfont_size=12
            ))
            
            fig.update_layout(
                title={
                    'text': 'Distribuição Sazonal de Visitantes',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20}
                },
                height=400,
                template='plotly_white'
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id="seasonal_chart")
            
        except Exception as e:
            print(f"Erro ao criar gráfico sazonal: {e}")
            return ""
    
    def create_sustainability_dashboard(self, eco_data: Dict) -> str:
        """Cria dashboard de sustentabilidade"""
        if 'sustainability_analysis' not in eco_data:
            return ""
        
        try:
            sustain = eco_data['sustainability_analysis']
            
            # Cria subplots
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Distribuição por Sustentabilidade', 'Índice de Fragilidade'),
                specs=[[{'type': 'pie'}, {'type': 'bar'}]]
            )
            
            # Gráfico de pizza - sustentabilidade
            sustainability_labels = [
                'Alta Sustentabilidade',
                'Sustentabilidade Moderada', 
                'Requer Cuidados',
                'Alta Fragilidade'
            ]
            
            sustainability_values = [
                sustain.get('high_sustainability', 0),
                sustain.get('moderate_sustainability', 0),
                sustain.get('requires_care', 0),
                sustain.get('high_fragility', 0)
            ]
            
            fig.add_trace(
                go.Pie(
                    labels=sustainability_labels,
                    values=sustainability_values,
                    marker_colors=[self.angola_colors['success'], self.angola_colors['info'], 
                                 self.angola_colors['warning'], self.angola_colors['danger']]
                ),
                row=1, col=1
            )
            
            # Gráfico de barras - distribuição de fragilidade
            fragility_dist = sustain.get('fragility_distribution', {})
            fragility_indices = list(fragility_dist.keys())
            fragility_counts = list(fragility_dist.values())
            
            fig.add_trace(
                go.Bar(
                    x=[f"Índice {i}" for i in fragility_indices],
                    y=fragility_counts,
                    marker_color=self.angola_colors['accent'],
                    text=fragility_counts,
                    textposition='outside'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title={
                    'text': 'Dashboard de Sustentabilidade dos Sítios',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20}
                },
                height=500,
                template='plotly_white',
                showlegend=False
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id="sustainability_dashboard")
            
        except Exception as e:
            print(f"Erro ao criar dashboard de sustentabilidade: {e}")
            return ""
    
    def create_capacity_analysis_chart(self, eco_data: Dict) -> str:
        """Cria gráfico de análise de capacidade"""
        if 'capacity_analysis' not in eco_data:
            return ""
        
        try:
            capacity_analysis = eco_data['capacity_analysis']['by_range']
            
            ranges = list(capacity_analysis.keys())
            counts = list(capacity_analysis.values())
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=ranges,
                y=counts,
                marker_color=[self.angola_colors['info'], self.angola_colors['success'], 
                            self.angola_colors['warning'], self.angola_colors['primary']],
                text=counts,
                textposition='outside'
            ))
            
            fig.update_layout(
                title={
                    'text': 'Distribuição de Sítios por Capacidade',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18}
                },
                xaxis_title='Faixa de Capacidade (visitantes/dia)',
                yaxis_title='Número de Sítios',
                template='plotly_white',
                height=400,
                showlegend=False
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id="capacity_chart")
            
        except Exception as e:
            print(f"Erro ao criar gráfico de capacidade: {e}")
            return ""
    
    def create_kpi_dashboard(self, kpis: Dict) -> str:
        """Cria dashboard com KPIs principais"""
        try:
            # Extrai KPIs principais
            tourism_kpis = kpis.get('tourism_kpis', {})
            sustainability_kpis = kpis.get('sustainability_kpis', {})
            economic_kpis = kpis.get('economic_kpis', {})
            
            # Cria figura com múltiplos subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Visitantes Anuais vs. Capacidade',
                    'Score de Sustentabilidade',
                    'Distribuição Econômica',
                    'Métricas Gerais'
                ),
                specs=[
                    [{'type': 'bar'}, {'type': 'indicator'}],
                    [{'type': 'bar'}, {'type': 'scatter'}]
                ]
            )
            
            # Gráfico 1: Visitantes vs Capacidade
            fig.add_trace(
                go.Bar(
                    x=['Visitantes Anuais', 'Capacidade Diária'],
                    y=[tourism_kpis.get('total_annual_visitors', 0), 
                       sustainability_kpis.get('total_eco_capacity', 0) * 365],
                    marker_color=[self.angola_colors['primary'], self.angola_colors['accent']],
                    name='Volume'
                ),
                row=1, col=1
            )
            
            # Gráfico 2: Indicador de Sustentabilidade
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=sustainability_kpis.get('average_sustainability_score', 0),
                    title={'text': "Score de Sustentabilidade"},
                    gauge={
                        'axis': {'range': [None, 10]},
                        'bar': {'color': self.angola_colors['success']},
                        'steps': [
                            {'range': [0, 5], 'color': self.angola_colors['danger']},
                            {'range': [5, 7.5], 'color': self.angola_colors['warning']},
                            {'range': [7.5, 10], 'color': self.angola_colors['success']}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 8
                        }
                    }
                ),
                row=1, col=2
            )
            
            # Gráfico 3: Métricas Econômicas
            economic_metrics = [
                'Receita Estimada (M AOA)',
                'Taxa Média (K AOA)', 
                'Score Distribuição'
            ]
            economic_values = [
                economic_kpis.get('estimated_annual_revenue', 0) / 1000000,
                economic_kpis.get('average_site_fee', 0) / 1000,
                economic_kpis.get('economic_distribution_score', 0)
            ]
            
            fig.add_trace(
                go.Bar(
                    x=economic_metrics,
                    y=economic_values,
                    marker_color=self.angola_colors['info'],
                    name='Economia'
                ),
                row=2, col=1
            )
            
            # Gráfico 4: Scatter plot de métricas gerais
            fig.add_trace(
                go.Scatter(
                    x=[tourism_kpis.get('foreign_visitor_percentage', 0)],
                    y=[tourism_kpis.get('average_stay_duration', 0)],
                    mode='markers+text',
                    text=['Angola Tourism'],
                    textposition='top center',
                    marker=dict(
                        size=sustainability_kpis.get('provinces_with_eco_sites', 1) * 10,
                        color=self.angola_colors['primary'],
                        opacity=0.7
                    ),
                    name='Perfil Turístico'
                ),
                row=2, col=2
            )
            
            fig.update_xaxes(title_text="% Visitantes Estrangeiros", row=2, col=2)
            fig.update_yaxes(title_text="Estadia Média (noites)", row=2, col=2)
            
            fig.update_layout(
                title={
                    'text': 'Dashboard de KPIs - SmartTour Angola',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 24}
                },
                height=700,
                template='plotly_white',
                showlegend=False
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id="kpi_dashboard")
            
        except Exception as e:
            print(f"Erro ao criar dashboard de KPIs: {e}")
            return ""
    
    def create_route_optimization_viz(self, route_data: Dict) -> str:
        """Visualiza rota otimizada"""
        if not route_data or 'sites' not in route_data:
            return ""
        
        try:
            sites = route_data['sites']
            
            # Prepara dados para mapa
            lats = [site['coordinates'][0] for site in sites]
            lons = [site['coordinates'][1] for site in sites]
            names = [site['name'] for site in sites]
            capacities = [site['daily_capacity'] for site in sites]
            
            fig = go.Figure()
            
            # Adiciona marcadores dos sítios
            fig.add_trace(go.Scattermapbox(
                lat=lats,
                lon=lons,
                mode='markers+text',
                marker=dict(
                    size=[cap/100 for cap in capacities],  # Tamanho proporcional à capacidade
                    color=self.angola_colors['primary'],
                    opacity=0.8
                ),
                text=names,
                textposition='top center',
                textfont=dict(size=10),
                name='Sítios da Rota'
            ))
            
            # Adiciona linha conectando os sítios
            fig.add_trace(go.Scattermapbox(
                lat=lats + [lats[0]],  # Volta ao primeiro ponto
                lon=lons + [lons[0]],
                mode='lines',
                line=dict(
                    width=3,
                    color=self.angola_colors['accent']
                ),
                name='Rota Otimizada'
            ))
            
            # Calcula centro do mapa
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
            
            fig.update_layout(
                title={
                    'text': f'Rota Otimizada - {route_data.get("province", "Angola")}',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18}
                },
                mapbox=dict(
                    accesstoken='pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2t0cGZxaHc0MXNmOTJubWpobjJhYTR0aSJ9.A2r7t2eZLpNjY8TE4EMxPQ',  # Token público do Mapbox
                    style='open-street-map',
                    center=dict(lat=center_lat, lon=center_lon),
                    zoom=7
                ),
                height=500,
                showlegend=True
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id="route_map")
            
        except Exception as e:
            print(f"Erro ao criar visualização de rota: {e}")
            return ""
    
    def generate_executive_chart(self, summary_data: Dict) -> str:
        """Gera gráfico executivo resumido"""
        try:
            if 'top_provinces' not in summary_data:
                return ""
            
            top_provinces = summary_data['top_provinces']
            
            provinces = list(top_provinces.keys())[:5]  # Top 5
            visitors = [data['visitors'] for data in top_provinces.values()][:5]
            foreign_shares = [data['foreign_share'] for data in top_provinces.values()][:5]
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Top 5 Províncias por Visitantes', 'Participação de Estrangeiros (%)'),
                specs=[[{'secondary_y': False}, {'secondary_y': False}]]
            )
            
            # Gráfico de barras - visitantes
            fig.add_trace(
                go.Bar(
                    x=provinces,
                    y=visitors,
                    marker_color=self.angola_colors['primary'],
                    text=[f"{v:,}" for v in visitors],
                    textposition='outside',
                    name='Visitantes'
                ),
                row=1, col=1
            )
            
            # Gráfico de barras - participação estrangeiros
            fig.add_trace(
                go.Bar(
                    x=provinces,
                    y=foreign_shares,
                    marker_color=self.angola_colors['accent'],
                    text=[f"{fs}%" for fs in foreign_shares],
                    textposition='outside',
                    name='% Estrangeiros'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title={
                    'text': 'Relatório Executivo - Principais Destinos',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20}
                },
                height=500,
                template='plotly_white',
                showlegend=False,
                xaxis=dict(tickangle=45)
            )
            
            return fig.to_html(include_plotlyjs='cdn', div_id="executive_chart")
            
        except Exception as e:
            print(f"Erro ao criar gráfico executivo: {e}")
            return ""
    
    def create_matplotlib_summary(self, kpis: Dict) -> str:
        """Cria gráfico resumo usando matplotlib (para exportar como imagem)"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('SmartTour Angola - Dashboard Resumo', fontsize=20, fontweight='bold')
            
            # Gráfico 1: KPIs Principais
            kpi_labels = ['Visitantes\nAnuais (K)', 'Sites\nSustentáveis (%)', 'Capacidade\nDiária (K)', 'Receita\nAnual (M AOA)']
            kpi_values = [
                kpis.get('tourism_kpis', {}).get('total_annual_visitors', 0) / 1000,
                kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0),
                kpis.get('sustainability_kpis', {}).get('total_eco_capacity', 0) / 1000,
                kpis.get('economic_kpis', {}).get('estimated_annual_revenue', 0) / 1000000
            ]
            
            bars1 = ax1.bar(kpi_labels, kpi_values, color=[self.angola_colors['primary'], 
                                                          self.angola_colors['success'],
                                                          self.angola_colors['info'], 
                                                          self.angola_colors['accent']])
            ax1.set_title('KPIs Principais', fontsize=14, fontweight='bold')
            ax1.tick_params(axis='x', rotation=45)
            
            # Adiciona valores nas barras
            for bar, value in zip(bars1, kpi_values):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            # Gráfico 2: Score de Sustentabilidade (gauge simulado)
            sustainability_score = kpis.get('sustainability_kpis', {}).get('average_sustainability_score', 0)
            
            theta = np.linspace(0, np.pi, 100)
            r = np.ones_like(theta)
            
            ax2.fill_between(theta, 0, r, where=(theta <= (sustainability_score/10 * np.pi)), 
                           color=self.angola_colors['success'], alpha=0.7)
            ax2.fill_between(theta, 0, r, where=(theta > (sustainability_score/10 * np.pi)), 
                           color='lightgray', alpha=0.3)
            ax2.set_ylim(0, 1.2)
            ax2.set_xlim(0, np.pi)
            ax2.set_title(f'Score de Sustentabilidade: {sustainability_score:.1f}/10', 
                         fontsize=14, fontweight='bold')
            ax2.axis('off')
            
            # Gráfico 3: Métricas Turísticas
            tourism_metrics = ['Duração Média\n(noites)', 'Visitantes\nEstrangeiros (%)', 'Variação\nSazonal (%)']
            tourism_values = [
                kpis.get('tourism_kpis', {}).get('average_stay_duration', 0),
                kpis.get('tourism_kpis', {}).get('foreign_visitor_percentage', 0),
                kpis.get('tourism_kpis', {}).get('seasonal_variation', 0)
            ]
            
            bars3 = ax3.bar(tourism_metrics, tourism_values, color=self.angola_colors['info'])
            ax3.set_title('Métricas de Turismo', fontsize=14, fontweight='bold')
            ax3.tick_params(axis='x', rotation=45)
            
            for bar, value in zip(bars3, tourism_values):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            # Gráfico 4: Distribuição por Sustentabilidade (pizza)
            sustainability_data = [
                kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0),
                100 - kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0)
            ]
            
            colors = [self.angola_colors['success'], self.angola_colors['danger']]
            wedges, texts, autotexts = ax4.pie(sustainability_data, 
                                              labels=['Sustentáveis', 'Requerem Atenção'],
                                              colors=colors, autopct='%1.1f%%', startangle=90)
            ax4.set_title('Distribuição de Sustentabilidade', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            # Converte para base64 para incorporar no HTML
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            buffer.close()
            plt.close(fig)
            
            html_img = f'<img src="data:image/png;base64,{image_base64}" style="max-width:100%; height:auto;" id="summary_chart"/>'
            
            return html_img
            
        except Exception as e:
            print(f"Erro ao criar gráfico resumo matplotlib: {e}")
            return ""
