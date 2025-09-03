"""
SmartTour - Data Models
Modelos de dados para análise de turismo sustentável
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import logging

class TouristData:
    """Classe para gerenciar dados de visitantes por província"""
    
    def __init__(self, data_path: str = None):
        self.data = None
        self.provinces = []
        self.years_range = []
        
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, data_path: str) -> None:
        """Carrega dados de visitantes de arquivo CSV"""
        try:
            self.data = pd.read_csv(data_path)
            self.data['date'] = pd.to_datetime(self.data['date'])
            self.provinces = list(self.data['province'].unique())
            self.years_range = list(self.data['year'].unique())
            logging.info(f"Dados carregados: {len(self.data)} registros de {len(self.provinces)} províncias")
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {e}")
            raise
    
    def get_province_stats(self, province: str) -> Dict:
        """Retorna estatísticas de uma província específica"""
        if self.data is None:
            return {}
        
        province_data = self.data[self.data['province'] == province]
        
        return {
            'total_visitors': province_data['visitors_total'].sum(),
            'avg_foreign_share': province_data['foreign_share'].mean(),
            'avg_stay_nights': province_data['avg_stay_nights'].mean(),
            'peak_months': province_data[province_data['season'] == 'peak']['month'].tolist(),
            'growth_rate': self.calculate_growth_rate(province_data)
        }
    
    def calculate_growth_rate(self, data: pd.DataFrame) -> float:
        """Calcula taxa de crescimento anual"""
        if len(data) < 2:
            return 0.0
        
        yearly_data = data.groupby('year')['visitors_total'].sum()
        if len(yearly_data) < 2:
            return 0.0
        
        first_year = yearly_data.iloc[0]
        last_year = yearly_data.iloc[-1]
        years_diff = len(yearly_data) - 1
        
        if first_year == 0:
            return 0.0
        
        growth_rate = ((last_year / first_year) ** (1/years_diff) - 1) * 100
        return round(growth_rate, 2)
    
    def get_seasonal_analysis(self) -> Dict:
        """Análise sazonal do turismo"""
        if self.data is None:
            return {}
        
        seasonal_data = self.data.groupby(['season', 'month']).agg({
            'visitors_total': 'mean',
            'foreign_share': 'mean'
        }).reset_index()
        
        return {
            'peak_season_avg': seasonal_data[seasonal_data['season'] == 'peak']['visitors_total'].mean(),
            'offpeak_season_avg': seasonal_data[seasonal_data['season'] == 'offpeak']['visitors_total'].mean(),
            'best_months': seasonal_data.nlargest(3, 'visitors_total')['month'].tolist(),
            'seasonal_data': seasonal_data.to_dict('records')
        }

class EcoSiteData:
    """Classe para gerenciar dados de sítios de ecoturismo"""
    
    def __init__(self, data_path: str = None):
        self.data = None
        self.sites_by_province = {}
        
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, data_path: str) -> None:
        """Carrega dados de sítios ecológicos"""
        try:
            self.data = pd.read_csv(data_path)
            self.sites_by_province = self.data.groupby('province')['site_name'].apply(list).to_dict()
            logging.info(f"Dados de sítios carregados: {len(self.data)} sítios")
        except Exception as e:
            logging.error(f"Erro ao carregar dados de sítios: {e}")
            raise
    
    def get_site_info(self, site_name: str) -> Dict:
        """Retorna informações de um sítio específico"""
        if self.data is None:
            return {}
        
        site_data = self.data[self.data['site_name'] == site_name]
        if site_data.empty:
            return {}
        
        site = site_data.iloc[0]
        return {
            'name': site['site_name'],
            'province': site['province'],
            'coordinates': (site['lat'], site['lon']),
            'fragility_index': site['fragility_index'],
            'daily_capacity': site['capacity_daily'],
            'entry_fee': site['fee_aoa'],
            'sustainability_level': self.get_sustainability_level(site['fragility_index'])
        }
    
    def get_sustainability_level(self, fragility_index: int) -> str:
        """Classifica nível de sustentabilidade baseado no índice de fragilidade"""
        if fragility_index <= 2:
            return "Alta Sustentabilidade"
        elif fragility_index <= 3:
            return "Sustentabilidade Moderada"
        elif fragility_index <= 4:
            return "Requer Cuidados"
        else:
            return "Alta Fragilidade"
    
    def recommend_sites_by_capacity(self, min_capacity: int = 500) -> List[Dict]:
        """Recomenda sítios baseado na capacidade mínima"""
        if self.data is None:
            return []
        
        suitable_sites = self.data[self.data['capacity_daily'] >= min_capacity]
        
        recommendations = []
        for _, site in suitable_sites.iterrows():
            recommendations.append({
                'name': site['site_name'],
                'province': site['province'],
                'capacity': site['capacity_daily'],
                'fragility': site['fragility_index'],
                'sustainability': self.get_sustainability_level(site['fragility_index']),
                'fee': site['fee_aoa']
            })
        
        # Ordena por menor fragilidade (mais sustentável) e maior capacidade
        recommendations.sort(key=lambda x: (x['fragility'], -x['capacity']))
        return recommendations

class RouteOptimizer:
    """Classe para otimização de rotas de ecoturismo"""
    
    def __init__(self, eco_sites_data: EcoSiteData, tourist_data: TouristData):
        self.eco_sites = eco_sites_data
        self.tourist_data = tourist_data
    
    def calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calcula distância aproximada entre duas coordenadas (fórmula haversine simplificada)"""
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Conversão aproximada para km (para Angola)
        lat_diff = abs(lat2 - lat1) * 111
        lon_diff = abs(lon2 - lon1) * 111 * np.cos(np.radians((lat1 + lat2) / 2))
        
        distance = np.sqrt(lat_diff**2 + lon_diff**2)
        return round(distance, 2)
    
    def create_sustainable_route(self, province: str, max_sites: int = 5, 
                                max_fragility: int = 3) -> Dict:
        """Cria uma rota sustentável para uma província"""
        if self.eco_sites.data is None:
            return {}
        
        # Filtra sítios da província com baixa fragilidade
        province_sites = self.eco_sites.data[
            (self.eco_sites.data['province'] == province) & 
            (self.eco_sites.data['fragility_index'] <= max_fragility)
        ]
        
        if province_sites.empty:
            return {'error': f'Nenhum sítio sustentável encontrado em {province}'}
        
        # Seleciona os melhores sítios (menor fragilidade, maior capacidade)
        selected_sites = province_sites.nsmallest(max_sites, 'fragility_index')
        
        route_info = {
            'province': province,
            'total_sites': len(selected_sites),
            'sites': [],
            'total_capacity': selected_sites['capacity_daily'].sum(),
            'avg_fragility': round(selected_sites['fragility_index'].mean(), 2),
            'total_cost': selected_sites['fee_aoa'].sum(),
            'estimated_duration': len(selected_sites) * 2  # 2 dias por sítio
        }
        
        # Adiciona detalhes de cada sítio
        for _, site in selected_sites.iterrows():
            site_info = self.eco_sites.get_site_info(site['site_name'])
            route_info['sites'].append(site_info)
        
        return route_info
    
    def analyze_tourism_impact(self, route: Dict) -> Dict:
        """Analisa impacto potencial de uma rota no turismo local"""
        if not route or 'province' not in route:
            return {}
        
        province_stats = self.tourist_data.get_province_stats(route['province'])
        
        impact_analysis = {
            'current_visitors': province_stats.get('total_visitors', 0),
            'route_capacity': route.get('total_capacity', 0),
            'sustainability_score': self.calculate_sustainability_score(route),
            'economic_impact': route.get('total_cost', 0) * 12,  # Estimativa anual
            'recommendations': []
        }
        
        # Gera recomendações baseadas na análise
        if impact_analysis['sustainability_score'] >= 8:
            impact_analysis['recommendations'].append("Rota altamente sustentável - Promover ativamente")
        elif impact_analysis['sustainability_score'] >= 6:
            impact_analysis['recommendations'].append("Rota moderadamente sustentável - Implementar com monitoramento")
        else:
            impact_analysis['recommendations'].append("Rota requer melhorias de sustentabilidade")
        
        capacity_utilization = (impact_analysis['current_visitors'] / 
                               (impact_analysis['route_capacity'] * 365)) * 100
        
        if capacity_utilization > 80:
            impact_analysis['recommendations'].append("Capacidade próxima do limite - Considerar limitação de visitantes")
        elif capacity_utilization < 30:
            impact_analysis['recommendations'].append("Capacidade subutilizada - Oportunidade de crescimento sustentável")
        
        return impact_analysis
    
    def calculate_sustainability_score(self, route: Dict) -> float:
        """Calcula pontuação de sustentabilidade da rota (0-10)"""
        if not route or 'avg_fragility' not in route:
            return 0.0
        
        # Pontuação baseada na fragilidade (invertida)
        fragility_score = max(0, 10 - (route['avg_fragility'] * 2))
        
        # Bonus por capacidade adequada
        capacity_bonus = min(2, route.get('total_capacity', 0) / 1000)
        
        # Penalidade por custo muito alto
        cost_penalty = min(1, route.get('total_cost', 0) / 50000)
        
        final_score = fragility_score + capacity_bonus - cost_penalty
        return round(max(0, min(10, final_score)), 1)
