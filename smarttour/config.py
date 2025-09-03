"""
SmartTour - Configuration Module
Configurações globais da aplicação
"""

import os
from pathlib import Path

class SmartTourConfig:
    """Configurações globais do SmartTour"""
    
    # Diretórios
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "Material_hackathon" / "Data_set_examplos"
    OUTPUT_DIR = BASE_DIR / "output"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Arquivos de dados
    VISITORS_DATA_FILE = "Visitors_by_Province__preview_.csv"
    ECO_SITES_DATA_FILE = "Eco_Sites__preview_.csv"
    REVIEWS_DATA_FILE = "Reviews__preview_.csv"
    RESERVATIONS_DATA_FILE = "Reservations__preview_.csv"
    ENVIRONMENTAL_DATA_FILE = "Environmental_Impact__preview_.csv"
    
    # Configurações de visualização
    ANGOLA_COLORS = {
        'primary': '#CE1126',    # Vermelho da bandeira
        'secondary': '#000000',  # Preto da bandeira
        'accent': '#FFCD00',     # Amarelo da bandeira
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8'
    }
    
    # Configurações de análise
    DEFAULT_MIN_CAPACITY = 500
    MAX_FRAGILITY_SUSTAINABLE = 3
    DEFAULT_MAX_SITES_ROUTE = 5
    
    # ODS (Objetivos de Desenvolvimento Sustentável) relacionados
    RELATED_SDGS = {
        8: "Trabalho Decente e Crescimento Econômico",
        11: "Cidades e Comunidades Sustentáveis", 
        12: "Consumo e Produção Responsáveis",
        13: "Ação contra a Mudança Global do Clima",
        15: "Vida Terrestre"
    }
    
    # Províncias de Angola
    ANGOLA_PROVINCES = [
        "Luanda", "Benguela", "Huíla", "Namibe", "Huambo",
        "Cabinda", "Malanje", "Bié", "Uíge", "Zaire",
        "Lunda Norte", "Lunda Sul", "Moxico", "Cuando Cubango",
        "Cuanza Norte", "Cuanza Sul", "Cunene", "Bengo"
    ]
    
    # Configurações de logging
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = 'INFO'
    
    # Thresholds para KPIs
    THRESHOLDS = {
        'sustainability_score_excellent': 8.0,
        'sustainability_score_good': 6.0,
        'foreign_visitor_min_target': 25.0,  # Percentual mínimo de visitantes estrangeiros
        'capacity_utilization_max': 80.0,    # Utilização máxima recomendada
        'capacity_utilization_min': 30.0,    # Utilização mínima para crescimento
    }
    
    @classmethod
    def ensure_directories(cls):
        """Garante que os diretórios necessários existam"""
        for dir_path in [cls.OUTPUT_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(exist_ok=True)
    
    @classmethod
    def get_data_file_path(cls, filename: str) -> Path:
        """Retorna caminho completo para arquivo de dados"""
        return cls.DATA_DIR / filename
    
    @classmethod
    def is_valid_province(cls, province_name: str) -> bool:
        """Verifica se o nome da província é válido"""
        return province_name in cls.ANGOLA_PROVINCES
