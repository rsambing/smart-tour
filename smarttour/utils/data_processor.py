"""
SmartTour - Data Processor
Processamento e análise de dados turísticos
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any
import os

class DataProcessor:
    """Classe principal para processamento de dados do SmartTour"""
    
    def __init__(self):
        self.data_cache = {}
        self.setup_logging()
    
    def setup_logging(self):
        """Configura logging para o processador"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def load_csv_data(self, file_path: str, cache_key: str = None) -> pd.DataFrame:
        """Carrega dados CSV com cache"""
        if cache_key and cache_key in self.data_cache:
            self.logger.info(f"Usando dados em cache para {cache_key}")
            return self.data_cache[cache_key]
        
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"Arquivo não encontrado: {file_path}")
                return pd.DataFrame()
            
            data = pd.read_csv(file_path)
            self.logger.info(f"Dados carregados: {file_path} - {len(data)} registros")
            
            if cache_key:
                self.data_cache[cache_key] = data
            
            return data
        
        except Exception as e:
            self.logger.error(f"Erro ao carregar {file_path}: {e}")
            return pd.DataFrame()
    
    def process_visitor_data(self, data: pd.DataFrame) -> Dict:
        """Processa dados de visitantes e gera insights"""
        if data.empty:
            return {'error': 'Dados de visitantes não disponíveis'}
        
        try:
            # Conversões de tipo
            data['date'] = pd.to_datetime(data['date'])
            data['year'] = data['year'].astype(int)
            data['month'] = data['month'].astype(int)
            
            # Análises básicas
            insights = {
                'overview': {
                    'total_records': len(data),
                    'provinces_count': data['province'].nunique(),
                    'date_range': {
                        'start': data['date'].min().strftime('%Y-%m-%d'),
                        'end': data['date'].max().strftime('%Y-%m-%d')
                    },
                    'total_visitors': int(data['visitors_total'].sum())
                },
                'provinces': {},
                'seasonal_patterns': {},
                'growth_trends': {}
            }
            
            # Análise por província
            for province in data['province'].unique():
                province_data = data[data['province'] == province]
                insights['provinces'][province] = {
                    'total_visitors': int(province_data['visitors_total'].sum()),
                    'avg_foreign_share': round(province_data['foreign_share'].mean(), 3),
                    'avg_stay_nights': round(province_data['avg_stay_nights'].mean(), 2),
                    'peak_season_visitors': int(province_data[province_data['season'] == 'peak']['visitors_total'].sum()),
                    'offpeak_season_visitors': int(province_data[province_data['season'] == 'offpeak']['visitors_total'].sum())
                }
            
            # Padrões sazonais
            seasonal_data = data.groupby('season').agg({
                'visitors_total': ['sum', 'mean'],
                'foreign_share': 'mean',
                'avg_stay_nights': 'mean'
            }).round(2)
            
            insights['seasonal_patterns'] = {
                'peak_season': {
                    'total_visitors': int(seasonal_data.loc['peak', ('visitors_total', 'sum')]),
                    'avg_visitors_per_record': int(seasonal_data.loc['peak', ('visitors_total', 'mean')]),
                    'avg_foreign_share': float(seasonal_data.loc['peak', ('foreign_share', 'mean')]),
                    'avg_stay_nights': float(seasonal_data.loc['peak', ('avg_stay_nights', 'mean')])
                },
                'offpeak_season': {
                    'total_visitors': int(seasonal_data.loc['offpeak', ('visitors_total', 'sum')]),
                    'avg_visitors_per_record': int(seasonal_data.loc['offpeak', ('visitors_total', 'mean')]),
                    'avg_foreign_share': float(seasonal_data.loc['offpeak', ('foreign_share', 'mean')]),
                    'avg_stay_nights': float(seasonal_data.loc['offpeak', ('avg_stay_nights', 'mean')])
                }
            }
            
            # Tendências de crescimento
            yearly_data = data.groupby(['year', 'province'])['visitors_total'].sum().reset_index()
            for province in data['province'].unique():
                province_yearly = yearly_data[yearly_data['province'] == province]
                if len(province_yearly) > 1:
                    growth_rate = self.calculate_growth_rate(province_yearly['visitors_total'].tolist())
                    insights['growth_trends'][province] = growth_rate
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Erro ao processar dados de visitantes: {e}")
            return {'error': f'Erro no processamento: {str(e)}'}
    
    def process_eco_sites_data(self, data: pd.DataFrame) -> Dict:
        """Processa dados de sítios ecológicos"""
        if data.empty:
            return {'error': 'Dados de sítios ecológicos não disponíveis'}
        
        try:
            insights = {
                'overview': {
                    'total_sites': len(data),
                    'provinces_covered': data['province'].nunique(),
                    'total_daily_capacity': int(data['capacity_daily'].sum()),
                    'avg_fragility_index': round(data['fragility_index'].mean(), 2)
                },
                'by_province': {},
                'sustainability_analysis': {},
                'capacity_analysis': {}
            }
            
            # Análise por província
            for province in data['province'].unique():
                province_data = data[data['province'] == province]
                insights['by_province'][province] = {
                    'sites_count': len(province_data),
                    'total_capacity': int(province_data['capacity_daily'].sum()),
                    'avg_fragility': round(province_data['fragility_index'].mean(), 2),
                    'avg_fee': round(province_data['fee_aoa'].mean(), 2),
                    'sites': province_data['site_name'].tolist()
                }
            
            # Análise de sustentabilidade
            fragility_distribution = data['fragility_index'].value_counts().sort_index()
            insights['sustainability_analysis'] = {
                'high_sustainability': int(len(data[data['fragility_index'] <= 2])),
                'moderate_sustainability': int(len(data[data['fragility_index'] == 3])),
                'requires_care': int(len(data[data['fragility_index'] == 4])),
                'high_fragility': int(len(data[data['fragility_index'] >= 5])),
                'fragility_distribution': fragility_distribution.to_dict()
            }
            
            # Análise de capacidade
            capacity_ranges = pd.cut(data['capacity_daily'], 
                                   bins=[0, 500, 1000, 1500, float('inf')], 
                                   labels=['Pequeno (≤500)', 'Médio (501-1000)', 
                                          'Grande (1001-1500)', 'Muito Grande (>1500)'])
            
            insights['capacity_analysis'] = {
                'by_range': capacity_ranges.value_counts().to_dict(),
                'highest_capacity': {
                    'site': data.loc[data['capacity_daily'].idxmax(), 'site_name'],
                    'capacity': int(data['capacity_daily'].max()),
                    'province': data.loc[data['capacity_daily'].idxmax(), 'province']
                },
                'most_affordable': {
                    'site': data.loc[data['fee_aoa'].idxmin(), 'site_name'],
                    'fee': int(data['fee_aoa'].min()),
                    'province': data.loc[data['fee_aoa'].idxmin(), 'province']
                }
            }
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Erro ao processar dados de sítios: {e}")
            return {'error': f'Erro no processamento: {str(e)}'}
    
    def calculate_growth_rate(self, values: List[float]) -> float:
        """Calcula taxa de crescimento composta"""
        if len(values) < 2 or values[0] == 0:
            return 0.0
        
        try:
            periods = len(values) - 1
            growth_rate = ((values[-1] / values[0]) ** (1/periods) - 1) * 100
            return round(growth_rate, 2)
        except:
            return 0.0
    
    def generate_kpis(self, visitor_data: Dict, eco_data: Dict) -> Dict:
        """Gera KPIs principais do SmartTour"""
        try:
            kpis = {
                'tourism_kpis': {
                    'total_annual_visitors': 0,
                    'foreign_visitor_percentage': 0,
                    'average_stay_duration': 0,
                    'seasonal_variation': 0,
                    'province_diversity_index': 0
                },
                'sustainability_kpis': {
                    'sustainable_sites_percentage': 0,
                    'total_eco_capacity': 0,
                    'average_sustainability_score': 0,
                    'provinces_with_eco_sites': 0
                },
                'economic_kpis': {
                    'estimated_annual_revenue': 0,
                    'average_site_fee': 0,
                    'economic_distribution_score': 0
                }
            }
            
            # KPIs de Turismo
            if 'overview' in visitor_data:
                overview = visitor_data['overview']
                kpis['tourism_kpis']['total_annual_visitors'] = overview.get('total_visitors', 0) * 12  # Estimativa anual
                
                # Percentual médio de estrangeiros
                if 'provinces' in visitor_data:
                    foreign_shares = [p.get('avg_foreign_share', 0) for p in visitor_data['provinces'].values()]
                    kpis['tourism_kpis']['foreign_visitor_percentage'] = round(np.mean(foreign_shares) * 100, 1)
                
                # Duração média de estadia
                if 'provinces' in visitor_data:
                    stay_durations = [p.get('avg_stay_nights', 0) for p in visitor_data['provinces'].values()]
                    kpis['tourism_kpis']['average_stay_duration'] = round(np.mean(stay_durations), 1)
                
                # Variação sazonal
                if 'seasonal_patterns' in visitor_data:
                    peak = visitor_data['seasonal_patterns'].get('peak_season', {}).get('total_visitors', 0)
                    offpeak = visitor_data['seasonal_patterns'].get('offpeak_season', {}).get('total_visitors', 0)
                    if offpeak > 0:
                        kpis['tourism_kpis']['seasonal_variation'] = round((peak - offpeak) / offpeak * 100, 1)
                
                kpis['tourism_kpis']['province_diversity_index'] = overview.get('provinces_count', 0)
            
            # KPIs de Sustentabilidade
            if 'overview' in eco_data:
                eco_overview = eco_data['overview']
                kpis['sustainability_kpis']['total_eco_capacity'] = eco_overview.get('total_daily_capacity', 0)
                kpis['sustainability_kpis']['provinces_with_eco_sites'] = eco_overview.get('provinces_covered', 0)
                
                if 'sustainability_analysis' in eco_data:
                    sustain_analysis = eco_data['sustainability_analysis']
                    total_sites = eco_overview.get('total_sites', 1)
                    sustainable_sites = (sustain_analysis.get('high_sustainability', 0) + 
                                       sustain_analysis.get('moderate_sustainability', 0))
                    kpis['sustainability_kpis']['sustainable_sites_percentage'] = round(
                        (sustainable_sites / total_sites) * 100, 1)
                
                # Score de sustentabilidade (baseado na fragilidade invertida)
                avg_fragility = eco_overview.get('avg_fragility_index', 3)
                kpis['sustainability_kpis']['average_sustainability_score'] = round(10 - (avg_fragility * 2), 1)
            
            # KPIs Econômicos
            if 'by_province' in eco_data:
                fees = []
                total_revenue = 0
                for province_info in eco_data['by_province'].values():
                    fees.append(province_info.get('avg_fee', 0))
                    total_revenue += province_info.get('total_capacity', 0) * province_info.get('avg_fee', 0)
                
                kpis['economic_kpis']['average_site_fee'] = round(np.mean(fees) if fees else 0, 2)
                kpis['economic_kpis']['estimated_annual_revenue'] = int(total_revenue * 365 * 0.7)  # 70% ocupação estimada
                
                # Score de distribuição econômica
                province_count = len(eco_data['by_province'])
                kpis['economic_kpis']['economic_distribution_score'] = min(10, province_count * 1.5)
            
            return kpis
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar KPIs: {e}")
            return {}
    
    def create_summary_report(self, visitor_insights: Dict, eco_insights: Dict, kpis: Dict) -> Dict:
        """Cria relatório executivo resumido"""
        try:
            report = {
                'executive_summary': {
                    'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'total_provinces_analyzed': 0,
                    'key_findings': [],
                    'recommendations': []
                },
                'performance_metrics': kpis,
                'top_provinces': {},
                'sustainability_highlights': {},
                'growth_opportunities': []
            }
            
            # Resumo executivo
            if 'overview' in visitor_insights:
                report['executive_summary']['total_provinces_analyzed'] = visitor_insights['overview'].get('provinces_count', 0)
            
            # Top províncias por visitantes
            if 'provinces' in visitor_insights:
                sorted_provinces = sorted(
                    visitor_insights['provinces'].items(),
                    key=lambda x: x[1].get('total_visitors', 0),
                    reverse=True
                )[:5]
                
                report['top_provinces'] = {
                    name: {
                        'visitors': data.get('total_visitors', 0),
                        'foreign_share': round(data.get('avg_foreign_share', 0) * 100, 1),
                        'avg_stay': data.get('avg_stay_nights', 0)
                    }
                    for name, data in sorted_provinces
                }
            
            # Destaques de sustentabilidade
            if 'sustainability_analysis' in eco_insights:
                sustain = eco_insights['sustainability_analysis']
                report['sustainability_highlights'] = {
                    'highly_sustainable_sites': sustain.get('high_sustainability', 0),
                    'sites_requiring_care': sustain.get('requires_care', 0) + sustain.get('high_fragility', 0),
                    'sustainability_percentage': round(
                        (sustain.get('high_sustainability', 0) + sustain.get('moderate_sustainability', 0)) /
                        max(1, sum(sustain.get('fragility_distribution', {}).values())) * 100, 1
                    )
                }
            
            # Achados principais
            report['executive_summary']['key_findings'] = [
                f"Total de {kpis.get('tourism_kpis', {}).get('total_annual_visitors', 0):,} visitantes anuais estimados",
                f"{kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0)}% dos sítios são sustentáveis",
                f"Capacidade diária total de {kpis.get('sustainability_kpis', {}).get('total_eco_capacity', 0):,} visitantes",
                f"Receita anual estimada: {kpis.get('economic_kpis', {}).get('estimated_annual_revenue', 0):,} AOA"
            ]
            
            # Recomendações
            sustainability_score = kpis.get('sustainability_kpis', {}).get('average_sustainability_score', 0)
            if sustainability_score < 5:
                report['executive_summary']['recommendations'].append(
                    "Priorizar melhoria da sustentabilidade dos sítios com alta fragilidade"
                )
            
            foreign_percentage = kpis.get('tourism_kpis', {}).get('foreign_visitor_percentage', 0)
            if foreign_percentage < 25:
                report['executive_summary']['recommendations'].append(
                    "Desenvolver estratégias de marketing internacional"
                )
            
            if len(report['top_provinces']) < 3:
                report['executive_summary']['recommendations'].append(
                    "Expandir oferta turística para mais províncias"
                )
            
            return report
            
        except Exception as e:
            self.logger.error(f"Erro ao criar relatório: {e}")
            return {'error': f'Erro na criação do relatório: {str(e)}'}


class DataValidator:
    """Classe para validação de dados de entrada"""
    
    @staticmethod
    def validate_visitor_data(data: pd.DataFrame) -> List[str]:
        """Valida dados de visitantes"""
        errors = []
        
        required_columns = ['date', 'year', 'month', 'province', 'visitors_total', 'foreign_share', 'avg_stay_nights', 'season']
        
        for col in required_columns:
            if col not in data.columns:
                errors.append(f"Coluna obrigatória ausente: {col}")
        
        if 'visitors_total' in data.columns:
            if (data['visitors_total'] < 0).any():
                errors.append("Valores negativos encontrados em visitors_total")
        
        if 'foreign_share' in data.columns:
            if (data['foreign_share'] < 0).any() or (data['foreign_share'] > 1).any():
                errors.append("foreign_share deve estar entre 0 e 1")
        
        return errors
    
    @staticmethod
    def validate_eco_sites_data(data: pd.DataFrame) -> List[str]:
        """Valida dados de sítios ecológicos"""
        errors = []
        
        required_columns = ['site_name', 'province', 'lat', 'lon', 'fragility_index', 'capacity_daily', 'fee_aoa']
        
        for col in required_columns:
            if col not in data.columns:
                errors.append(f"Coluna obrigatória ausente: {col}")
        
        if 'fragility_index' in data.columns:
            if (data['fragility_index'] < 1).any() or (data['fragility_index'] > 5).any():
                errors.append("fragility_index deve estar entre 1 e 5")
        
        if 'capacity_daily' in data.columns:
            if (data['capacity_daily'] < 0).any():
                errors.append("capacity_daily não pode ser negativo")
        
        return errors
