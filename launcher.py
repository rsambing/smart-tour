#!/usr/bin/env python3
"""
SmartTour Angola - Launcher
Escolha entre interface desktop (tkinter) ou web (Flask)
"""

import sys
import os
import subprocess
from pathlib import Path

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Imprime banner do SmartTour Angola"""
    print("🇦🇴" + "="*60 + "🇦🇴")
    print("   SMARTTOUR ANGOLA - LAUNCHER")
    print("   Sistema de Análise de Turismo Sustentável")
    print("   Descentralização e Ecoturismo | FTL Bootcamp")
    print("🇦🇴" + "="*60 + "🇦🇴")
    print()

def print_menu():
    """Imprime menu de opções"""
    print("📱 ESCOLHA A INTERFACE:")
    print()
    print("1. 🖥️  Interface Desktop (tkinter)")
    print("   • Aplicação nativa com tema escuro")
    print("   • KPIs em tempo real")
    print("   • Design moderno ecológico")
    print()
    print("2. 🌐 Interface Web (Flask)")
    print("   • Acesso via navegador")
    print("   • Responsiva e moderna")
    print("   • Upload de arquivos")
    print()
    print("3. 🚀 Análise Rápida (Terminal)")
    print("   • Execução direta no terminal")
    print("   • Dados padrão")
    print("   • Geração automática de relatório")
    print()
    print("4. ❌ Sair")
    print()

def run_desktop():
    """Executa interface desktop"""
    print("🖥️ Iniciando interface desktop...")
    print("📋 Verificando dependências...")
    
    try:
        import tkinter
        print("✅ tkinter disponível")
        
        # Testar se interface gráfica funciona
        try:
            test_root = tkinter.Tk()
            test_root.destroy()
            print("✅ Interface gráfica OK")
        except Exception as e:
            print(f"❌ Problema com interface gráfica: {e}")
            print("� Tentando versão segura...")
        
        print("�🚀 Executando SmartTour Desktop...")
        
        # Tentar versão segura primeiro
        if os.path.exists("smarttour_desktop_safe.py"):
            subprocess.run([sys.executable, "smarttour_desktop_safe.py"])
        else:
            subprocess.run([sys.executable, "smarttour_desktop.py"])
        
    except ImportError:
        print("❌ tkinter não está disponível")
        print("💡 Para instalar: sudo apt install python3-tk")
        input("\nPressione Enter para continuar...")

def run_web():
    """Executa interface web"""
    print("🌐 Iniciando interface web...")
    print("📋 Verificando dependências...")
    
    try:
        import flask
        print("✅ Flask disponível")
        
        print("🚀 Executando SmartTour Web...")
        print("📱 Acesse: http://localhost:5000")
        print("🛑 Pressione Ctrl+C para parar o servidor")
        print()
        
        subprocess.run([sys.executable, "smarttour_web.py"])
        
    except ImportError:
        print("❌ Flask não está disponível")
        print("💡 Para instalar: pip install flask")
        input("\nPressione Enter para continuar...")

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
                run_desktop()
            
            elif choice == '2':
                clear_screen()
                print_banner()
                run_web()
            
            elif choice == '3':
                clear_screen()
                print_banner()
                run_terminal()
            
            elif choice == '4':
                clear_screen()
                print("👋 Obrigado por usar o SmartTour Angola!")
                print("🇦🇴 Até logo!")
                break
            
            else:
                print("❌ Opção inválida! Escolha entre 1-4.")
                input("Pressione Enter para continuar...")
        
        except KeyboardInterrupt:
            clear_screen()
            print("\n👋 Saindo do SmartTour Angola...")
            print("🇦🇴 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
