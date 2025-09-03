"""
SmartTour Angola - Demonstração Completa
Demo script mostrando todas as funcionalidades
"""

from smarttour_app import smarttour_app
import json

def main_demo():
    """Demonstração completa do SmartTour"""
    print("🇦🇴 SMARTTOUR ANGOLA - DEMONSTRAÇÃO")
    print("=" * 60)
    
    # 1. Inicialização
    print("🚀 1. INICIALIZAÇÃO DO SISTEMA")
    print("-" * 30)
    smarttour_app.load_sample_data()
    smarttour_app.perform_analysis()
    
    status = smarttour_app.get_status()
    print(f"✅ Províncias analisadas: {status['provinces_available']}")
    print(f"✅ Sítios ecológicos: {status['eco_sites_available']}")
    print(f"✅ Análise completa: {status['analysis_completed']}")
    
    # 2. KPIs Principais
    print(f"\n📈 2. KPIs PRINCIPAIS")
    print("-" * 30)
    kpis = smarttour_app.kpis
    
    tourism_kpis = kpis.get('tourism_kpis', {})
    sustainability_kpis = kpis.get('sustainability_kpis', {})
    economic_kpis = kpis.get('economic_kpis', {})
    
    print(f"🎯 TURISMO:")
    print(f"  • Visitantes anuais: {tourism_kpis.get('total_annual_visitors', 0):,}")
    print(f"  • % Estrangeiros: {tourism_kpis.get('foreign_visitor_percentage', 0):.1f}%")
    print(f"  • Estadia média: {tourism_kpis.get('average_stay_duration', 0):.1f} noites")
    print(f"  • Variação sazonal: {tourism_kpis.get('seasonal_variation', 0):.1f}%")
    
    print(f"\n🌱 SUSTENTABILIDADE:")
    print(f"  • Sites sustentáveis: {sustainability_kpis.get('sustainable_sites_percentage', 0):.1f}%")
    print(f"  • Score médio: {sustainability_kpis.get('average_sustainability_score', 0):.1f}/10")
    print(f"  • Capacidade diária: {sustainability_kpis.get('total_eco_capacity', 0):,}")
    print(f"  • Províncias cobertas: {sustainability_kpis.get('provinces_with_eco_sites', 0)}")
    
    print(f"\n💰 ECONÔMICO:")
    print(f"  • Receita estimada: {economic_kpis.get('estimated_annual_revenue', 0):,} AOA")
    print(f"  • Taxa média: {economic_kpis.get('average_site_fee', 0):,} AOA")
    print(f"  • Score distribuição: {economic_kpis.get('economic_distribution_score', 0):.1f}/10")
    
    # 3. Análise por Província
    print(f"\n🗺️  3. ANÁLISE POR PROVÍNCIA")
    print("-" * 30)
    
    provinces = smarttour_app.tourist_data.provinces[:3]  # Top 3 províncias
    for province in provinces:
        analysis = smarttour_app.get_province_analysis(province)
        tourism_stats = analysis.get('tourism_stats', {})
        
        print(f"\n📍 {province.upper()}:")
        print(f"  • Visitantes: {tourism_stats.get('total_visitors', 0):,}")
        print(f"  • % Estrangeiros: {tourism_stats.get('avg_foreign_share', 0) * 100:.1f}%")
        print(f"  • Sítios ecológicos: {len(analysis.get('eco_sites', []))}")
        print(f"  • Score sustentabilidade: {analysis.get('sustainability_score', 0):.1f}/10")
    
    # 4. Top Sítios Ecológicos
    print(f"\n🌳 4. TOP SÍTIOS ECOLÓGICOS")
    print("-" * 30)
    
    eco_insights = smarttour_app.eco_insights
    for province, info in list(eco_insights.get('by_province', {}).items())[:3]:
        print(f"\n🏛️  {province}:")
        print(f"  • Número de sítios: {info.get('sites_count', 0)}")
        print(f"  • Capacidade total: {info.get('total_capacity', 0):,}/dia")
        print(f"  • Fragilidade média: {info.get('avg_fragility', 0):.1f}/5")
        print(f"  • Taxa média: {info.get('avg_fee', 0):,} AOA")
        
        sites = info.get('sites', [])[:2]  # Top 2 sites
        for site in sites:
            print(f"    - {site}")
    
    # 5. Recomendações Estratégicas
    print(f"\n🎯 5. RECOMENDAÇÕES ESTRATÉGICAS")
    print("-" * 30)
    
    summary = smarttour_app.summary_report
    recommendations = summary.get('executive_summary', {}).get('recommendations', [])
    
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    # 6. Próximos Passos
    print(f"\n🚀 6. PRÓXIMOS PASSOS")
    print("-" * 30)
    print("  1. 📊 Implementar dashboard em tempo real")
    print("  2. 🗺️  Adicionar mapas interativos")
    print("  3. 📱 Desenvolver versão mobile")
    print("  4. 🤖 Integrar machine learning")
    print("  5. 🌐 Conectar com APIs externas")
    print("  6. 📈 Expandir base de dados")
    
    # 7. Conclusão
    print(f"\n🏆 7. CONCLUSÃO")
    print("-" * 30)
    print("✅ SmartTour Angola está operacional!")
    print("✅ Sistema pronto para análise de turismo sustentável")
    print("✅ Dados processados e KPIs gerados")
    print("✅ Interface GUI disponível")
    print("✅ Relatórios exportáveis")
    
    print(f"\n{'=' * 60}")
    print("🌍 SmartTour Angola - Transformando Dados em Turismo Sustentável")
    print("🎯 Desenvolvido para FTL Bootcamp Hackathon")
    print("👑 Team Leader: Reinaldo Sambinga - Grupo 2")
    print("📅 Data: Setembro 2025")
    
    return True

if __name__ == "__main__":
    try:
        main_demo()
        print("\n🎉 Demonstração concluída com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()
