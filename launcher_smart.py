#!/usr/bin/env python3
"""
SmartTour Angola - Launcher Inteligente
Detecta problemas e redireciona para melhor interface disponível
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
    print("   SMARTTOUR ANGOLA - LAUNCHER INTELIGENTE")
    print("   Sistema de Análise de Turismo Sustentável")
    print("   Descentralização e Ecoturismo | FTL Bootcamp")
    print("🇦🇴" + "="*60 + "🇦🇴")
    print()

def test_desktop_availability():
    """Testa se interface desktop está disponível"""
    try:
        import tkinter
        # Teste básico de criação de janela
        root = tkinter.Tk()
        root.withdraw()  # Esconder janela
        root.destroy()
        return True
    except Exception as e:
        return False

def test_web_dependencies():
    """Testa se dependências web estão disponíveis"""
    try:
        import flask
        return True
    except ImportError:
        return False

def print_smart_menu():
    """Imprime menu inteligente baseado no que está disponível"""
    
    desktop_ok = test_desktop_availability()
    web_ok = test_web_dependencies()
    
    print("🤖 DETECÇÃO AUTOMÁTICA DE INTERFACES:")
    print()
    
    if web_ok:
        print("✅ 1. 🌐 Interface Web (RECOMENDADA)")
        print("   • Funcional e testada")
        print("   • Acesso via navegador")
        print("   • Design moderno responsivo")
        print("   • Upload de arquivos seguro")
    else:
        print("❌ 1. 🌐 Interface Web")
        print("   • Flask não instalado")
        print("   • Execute: pip install flask")
    
    print()
    
    if desktop_ok:
        print("⚠️  2. 🖥️  Interface Desktop (EXPERIMENTAL)")
        print("   • Pode ter problemas de compatibilidade")
        print("   • Use apenas se web não funcionar")
    else:
        print("❌ 2. 🖥️  Interface Desktop")
        print("   • tkinter não disponível")
        print("   • Execute: sudo apt install python3-tk")
    
    print()
    print("✅ 3. 🚀 Análise Rápida (SEMPRE FUNCIONA)")
    print("   • Execução direta no terminal")
    print("   • Dados padrão inclusos")
    print("   • Geração automática de relatório HTML")
    
    print()
    print("4. ❌ Sair")
    print()
    
    # Sugestão inteligente
    if web_ok:
        print("💡 RECOMENDAÇÃO: Use a Interface Web (opção 1) - é a mais estável!")
    elif desktop_ok:
        print("💡 RECOMENDAÇÃO: Use a Análise Rápida (opção 3) - mais confiável!")
    else:
        print("💡 RECOMENDAÇÃO: Instale dependências ou use Análise Rápida (opção 3)")
    
    return web_ok, desktop_ok

def run_web():
    """Executa interface web"""
    clear_screen()
    print_banner()
    print("🌐 Iniciando Interface Web...")
    print("📋 Verificando dependências...")
    
    if not test_web_dependencies():
        print("❌ Flask não está disponível")
        print("💡 Para instalar: pip install flask")
        input("\nPressione Enter para continuar...")
        return
    
    print("✅ Flask disponível")
    print("🚀 Executando SmartTour Web...")
    print("📱 Interface será aberta em: http://localhost:5000")
    print("🛑 Pressione Ctrl+C para parar o servidor")
    print()
    
    try:
        subprocess.run([sys.executable, "smarttour_web.py"])
    except KeyboardInterrupt:
        print("\n👋 Servidor web encerrado")
    except Exception as e:
        print(f"❌ Erro: {e}")
        input("\nPressione Enter para continuar...")

def run_desktop():
    """Executa interface desktop com fallback"""
    clear_screen()
    print_banner()
    print("🖥️ Iniciando Interface Desktop...")
    print("⚠️  AVISO: Interface experimental, pode ter problemas")
    print()
    
    if not test_desktop_availability():
        print("❌ Interface desktop não disponível")
        print("💡 Para instalar: sudo apt install python3-tk")
        print("\n🌐 Alternativa: Use a Interface Web")
        input("\nPressione Enter para continuar...")
        return
    
    print("🔍 Tentando executar interface desktop...")
    
    try:
        # Tentar versão segura primeiro
        if os.path.exists("smarttour_desktop_safe.py"):
            result = subprocess.run([sys.executable, "smarttour_desktop_safe.py"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print("❌ Interface desktop apresentou problemas")
                print(f"Erro: {result.stderr}")
                print("\n💡 SOLUÇÃO: Use a Interface Web que está funcionando perfeitamente!")
                print("Execute: python3 smarttour_web.py")
            else:
                print("✅ Interface desktop executada com sucesso")
        else:
            print("❌ Arquivo de interface desktop não encontrado")
    
    except subprocess.TimeoutExpired:
        print("⏱️ Interface desktop demorou demais para responder")
        print("💡 RECOMENDAÇÃO: Use a Interface Web (mais estável)")
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        print("💡 SOLUÇÃO: Use a Interface Web")
    
    input("\nPressione Enter para continuar...")

def run_terminal():
    """Executa análise rápida no terminal"""
    clear_screen()
    print_banner()
    print("🚀 Executando Análise Rápida...")
    print("📊 Usando dados padrão do hackathon")
    print("⏱️  Aguarde, processando...")
    print()
    
    try:
        result = subprocess.run([sys.executable, "smarttour_integrated.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Análise concluída com sucesso!")
            print()
            print("📋 SAÍDA DO SISTEMA:")
            print("-" * 50)
            print(result.stdout)
            print("-" * 50)
            print()
            print("📄 Relatório gerado: smarttour_angola_report.html")
            
            # Perguntar se quer abrir o relatório
            choice = input("🌐 Deseja abrir o relatório no navegador? (s/n): ").lower()
            if choice in ['s', 'sim', 'y', 'yes']:
                import webbrowser
                report_path = Path("smarttour_angola_report.html")
                if report_path.exists():
                    webbrowser.open(f"file://{report_path.absolute()}")
                    print("📋 Relatório aberto no navegador!")
                else:
                    print("❌ Arquivo de relatório não encontrado")
        else:
            print("❌ Erro na execução da análise:")
            print(result.stderr)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    input("\nPressione Enter para continuar...")

def main():
    """Função principal com detecção inteligente"""
    
    while True:
        clear_screen()
        print_banner()
        web_ok, desktop_ok = print_smart_menu()
        
        try:
            choice = input("👉 Digite sua escolha (1-4): ").strip()
            
            if choice == '1':
                if web_ok:
                    run_web()
                else:
                    print("❌ Interface Web não disponível")
                    print("💡 Instale Flask: pip install flask")
                    input("Pressione Enter para continuar...")
            
            elif choice == '2':
                if desktop_ok:
                    run_desktop()
                else:
                    print("❌ Interface Desktop não disponível")
                    print("💡 Instale tkinter: sudo apt install python3-tk")
                    input("Pressione Enter para continuar...")
            
            elif choice == '3':
                run_terminal()
            
            elif choice == '4':
                clear_screen()
                print("👋 Obrigado por usar o SmartTour Angola!")
                print("🇦🇴 Desenvolvido para o FTL Bootcamp 2024")
                print("✨ Até logo!")
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
