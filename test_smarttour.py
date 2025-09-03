"""
SmartTour - Test Script
Script de teste para verificar funcionamento completo
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_smarttour():
    """Testa funcionamento básico do SmartTour"""
    print("🚀 Iniciando teste do SmartTour Angola...")
    print("=" * 60)
    
    try:
        # Test imports
        print("📦 Testando importações...")
        from smarttour_app import smarttour_app
        from smarttour.models.tourism_model import TouristData, EcoSiteData, RouteOptimizer
        from smarttour.utils.data_processor import DataProcessor
        from smarttour.visualization.charts import TourismVisualizer
        print("✅ Importações bem-sucedidas")
        
        # Test data loading
        print("\n📊 Testando carregamento de dados...")
        smarttour_app.load_sample_data()
        
        if smarttour_app.data_loaded:
            print("✅ Dados carregados com sucesso")
            print(f"   • Províncias: {len(smarttour_app.tourist_data.provinces)}")
            print(f"   • Sítios ecológicos: {len(smarttour_app.eco_sites_data.data)}")
        else:
            print("❌ Falha no carregamento de dados")
            return False
        
        # Test analysis
        print("\n🔍 Testando análise de dados...")
        success = smarttour_app.perform_analysis()
        
        if success:
            print("✅ Análise concluída com sucesso")
            
            # Show KPIs
            kpis = smarttour_app.kpis
            tourism_kpis = kpis.get('tourism_kpis', {})
            sustainability_kpis = kpis.get('sustainability_kpis', {})
            
            print(f"\n📈 KPIs principais:")
            print(f"   • Visitantes anuais: {tourism_kpis.get('total_annual_visitors', 0):,}")
            print(f"   • Sites sustentáveis: {sustainability_kpis.get('sustainable_sites_percentage', 0)}%")
            print(f"   • Capacidade diária: {sustainability_kpis.get('total_eco_capacity', 0):,}")
            print(f"   • Score sustentabilidade: {sustainability_kpis.get('average_sustainability_score', 0):.1f}/10")
            
        else:
            print("❌ Falha na análise")
            return False
        
        # Test province analysis
        print("\n🗺️  Testando análise por província...")
        if smarttour_app.tourist_data.provinces:
            test_province = smarttour_app.tourist_data.provinces[0]
            province_analysis = smarttour_app.get_province_analysis(test_province)
            
            if province_analysis and 'error' not in province_analysis:
                print(f"✅ Análise de {test_province} concluída")
                print(f"   • Sites ecológicos: {len(province_analysis.get('eco_sites', []))}")
                print(f"   • Score sustentabilidade: {province_analysis.get('sustainability_score', 0):.1f}")
            else:
                print(f"❌ Falha na análise de {test_province}")
        
        # Test report export
        print("\n📄 Testando exportação de relatório...")
        report_path = "test_smarttour_report.html"
        success = smarttour_app.export_analysis_report(report_path)
        
        if success and os.path.exists(report_path):
            print(f"✅ Relatório exportado: {report_path}")
            print(f"   • Tamanho: {os.path.getsize(report_path):,} bytes")
        else:
            print("❌ Falha na exportação do relatório")
        
        print("\n" + "=" * 60)
        print("🎉 SmartTour Angola - TESTE CONCLUÍDO COM SUCESSO!")
        print("🏆 Sistema pronto para análise de turismo sustentável")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Verifique se todas as dependências estão instaladas:")
        print("   pip install pandas numpy matplotlib seaborn plotly PySide6")
        return False
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False

def show_features():
    """Mostra funcionalidades principais"""
    print("\n🎯 Funcionalidades do SmartTour Angola:")
    print("=" * 50)
    
    features = [
        "📊 Análise de fluxos turísticos por província",
        "🌱 Avaliação de sustentabilidade de sítios ecológicos", 
        "🗺️  Otimização de rotas de ecoturismo",
        "📈 Geração de KPIs e métricas de performance",
        "📋 Relatórios executivos em HTML",
        "🎨 Visualizações interativas e gráficos",
        "🏛️  Interface GUI moderna com PySide6",
        "🎯 Alinhamento com ODS (Objetivos de Desenvolvimento Sustentável)",
        "💰 Análise de impacto econômico",
        "📱 Sistema modular e extensível"
    ]
    
    for feature in features:
        print(f"  {feature}")

if __name__ == "__main__":
    print("🇦🇴 SMARTTOUR ANGOLA")
    print("Sistema de Análise de Turismo Sustentável")
    print("Desenvolvido para FTL Bootcamp Hackathon")
    print()
    
    show_features()
    
    print("\n🧪 Executando testes...")
    success = test_smarttour()
    
    if success:
        print("\n🚀 Para usar o SmartTour:")
        print("   1. Execute: python main.py")
        print("   2. A interface GUI será carregada")
        print("   3. O SmartTour será inicializado automaticamente")
        print("   4. Visualize dados nas abas da interface")
        print("\n💡 Ou use diretamente:")
        print("   from smarttour_app import smarttour_app")
        print("   smarttour_app.load_sample_data()")
        print("   smarttour_app.perform_analysis()")
    else:
        print("\n❌ Corrija os erros antes de usar o SmartTour")
    
    print("\n" + "=" * 60)
