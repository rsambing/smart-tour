#!/usr/bin/env python3
"""
SmartTour Angola - Main Application
Sistema de Análise de Turismo Sustentável para Angola
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Função principal da aplicação"""
    print("🇦🇴 SMARTTOUR ANGOLA")
    print("Sistema de Análise de Turismo Sustentável")
    print("=" * 60)
    
    try:
        # Import SmartTour integrated
        from smarttour_integrated import SmartTourAngola
        
        print("📦 SmartTour carregado com sucesso!")
        
        # Create instance and load data
        smarttour = SmartTourAngola()
        
        print("📊 Carregando dados...")
        if smarttour.load_data():
            print("✅ Dados carregados!")
            status = smarttour.get_status()
            print(f"   • {status['provinces_available']} províncias")
            print(f"   • {status['eco_sites_available']} sítios ecológicos")
            
            # Perform analysis
            print("🔍 Executando análise...")
            success = smarttour.perform_analysis()
            
            if success:
                print("✅ Análise concluída!")
                
                # Show key metrics
                kpis = smarttour.kpis
                print("\n📈 KPIs Principais:")
                print(f"   • Visitantes anuais: {kpis.get('tourism_kpis', {}).get('total_annual_visitors', 0):,}")
                print(f"   • Sites sustentáveis: {kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0)}%")
                print(f"   • Score sustentabilidade: {kpis.get('sustainability_kpis', {}).get('average_sustainability_score', 0):.1f}/10")
                
                # Export report
                print("\n📄 Exportando relatório...")
                report_success = smarttour.export_report("smarttour_angola_report.html")
                
                if report_success:
                    print("✅ Relatório exportado: smarttour_angola_report.html")
                else:
                    print("⚠️ Relatório gerado com avisos")
                
                print("\n🎉 SmartTour Angola executado com sucesso!")
                print("📋 Abra o arquivo 'smarttour_angola_report.html' para ver os resultados")
                
            else:
                print("❌ Erro na análise")
                return False
        else:
            print("❌ Erro ao carregar dados")
            return False
            
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
