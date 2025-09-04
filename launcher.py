#!/usr/bin/env python3
"""
SmartTour Angola - Launcher Simplificado
Escolha entre as 3 interfaces: Terminal, Web e Desktop
"""

import sys
import os
import subprocess
from pathlib import Path

def clear_screen():
    """Limpa tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Banner principal"""
    print("🇦🇴" + "="*50 + "🇦🇴")
    print("      SMARTTOUR ANGOLA - LAUNCHER")
    print("   Sistema de Turismo Sustentável")
    print("🇦🇴" + "="*50 + "🇦🇴")
    print()

def print_menu():
    """Menu de opções"""
    print("📱 ESCOLHA SUA INTERFACE:")
    print()
    print("1. 🖥️  Terminal (Rápido)")
    print("   • Execução automática")
    print("   • Gera relatório HTML")
    print("   • Ideal para análise rápida")
    print()
    print("2. 🌐 Web (Recomendado)")
    print("   • Interface moderna no navegador")
    print("   • Upload de arquivos")
    print("   • Visualizações interativas")
    print()
    print("3. 🖱️  Desktop (GUI)")
    print("   • Interface gráfica nativa")
    print("   • Simples e funcional")
    print("   • Requer tkinter instalado")
    print()
    print("4. ❌ Sair")
    print()

def run_terminal():
    """Executa análise no terminal"""
    print("🚀 Executando análise rápida...")
    print("📊 Usando dados padrão do hackathon")
    print()
    
    try:
        subprocess.run([sys.executable, "smarttour_integrated.py"])
        print()
        print("✅ Análise concluída!")
        print("📄 Relatório gerado: smarttour_angola_report.html")
        
        # Perguntar se quer abrir o relatório
        choice = input("\n🌐 Deseja abrir o relatório no navegador? (s/n): ").lower()
        if choice in ['s', 'sim', 'y', 'yes']:
            import webbrowser
            report_path = Path("smarttour_angola_report.html")
            if report_path.exists():
                webbrowser.open(f"file://{report_path.absolute()}")
                print("📋 Relatório aberto no navegador!")
            else:
                print("❌ Arquivo de relatório não encontrado")
        
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
    
    input("\nPressione Enter para continuar...")

def run_web():
    """Executa versão web"""
    print("🌐 Iniciando SmartTour Web...")
    print("📱 Acesse: http://localhost:5000")
    print("🛑 Pressione Ctrl+C para parar")
    print()
    try:
        subprocess.run([sys.executable, "smarttour_web.py"])
    except FileNotFoundError:
        print("❌ Arquivo smarttour_web.py não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

def run_desktop():
    """Executa versão desktop"""
    print("🖥️ Iniciando SmartTour Desktop...")
    
    # Verifica se tkinter está disponível
    try:
        import tkinter
        print("✅ tkinter disponível")
    except ImportError:
        print("❌ tkinter não instalado")
        print("💡 Instale: sudo apt install python3-tk")
        return
    
    try:
        subprocess.run([sys.executable, "smarttour_desktop_clean.py"])
    except FileNotFoundError:
        print("❌ Arquivo smarttour_desktop_clean.py não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        try:
            choice = input("👉 Digite sua escolha (1-4): ").strip()
            
            if choice == '1':
                clear_screen()
                print_banner()
                run_terminal()
                input("\nPressione Enter para continuar...")
            
            elif choice == '2':
                clear_screen()
                print_banner()
                run_web()
                input("\nPressione Enter para continuar...")
            
            elif choice == '3':
                clear_screen()
                print_banner()
                run_desktop()
                input("\nPressione Enter para continuar...")
            
            elif choice == '4':
                clear_screen()
                print("👋 Obrigado por usar o SmartTour Angola!")
                print("🇦🇴 Até logo!")
                break
            
            else:
                print("❌ Opção inválida! Use 1, 2, 3 ou 4.")
                input("Pressione Enter para continuar...")
        
        except KeyboardInterrupt:
            clear_screen()
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
