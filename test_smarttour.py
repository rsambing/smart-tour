#!/usr/bin/env python3
"""
Test SmartTour Angola - Verificador Simples
Testa se tudo está funcionando
"""

import os
import sys

def test_files():
    """Testa se os arquivos essenciais existem"""
    files = [
        'smarttour_core.py',
        'smarttour_web.py', 
        'smarttour_desktop_clean.py',
        'smarttour_integrated.py',
        'launcher.py'
    ]
    
    print("📁 Verificando arquivos...")
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - AUSENTE")
            return False
    return True

def test_imports():
    """Testa se as dependências podem ser importadas"""
    print("\n📦 Verificando dependências...")
    
    try:
        import pandas as pd
        print("   ✅ pandas")
    except ImportError:
        print("   ❌ pandas - INSTALE: pip install pandas")
        return False
        
    try:
        import plotly.express as px
        print("   ✅ plotly")
    except ImportError:
        print("   ❌ plotly - INSTALE: pip install plotly")
        return False
        
    try:
        from flask import Flask
        print("   ✅ flask")
    except ImportError:
        print("   ❌ flask - INSTALE: pip install flask")
        return False
        
    try:
        import tkinter
        print("   ✅ tkinter")
    except ImportError:
        print("   ❌ tkinter - INSTALE: sudo apt install python3-tk")
        return False
        
    return True

def test_core():
    """Testa se o núcleo funciona"""
    print("\n🔧 Testando núcleo...")
    
    try:
        from smarttour_core import SmartTourCore
        print("   ✅ Import do núcleo")
        
        core = SmartTourCore()
        print("   ✅ Criação do núcleo")
        
        if core.load_data():
            print("   ✅ Carregamento de dados")
        else:
            print("   ❌ Erro no carregamento")
            return False
            
        if core.perform_analysis():
            print("   ✅ Análise completa")
            return True
        else:
            print("   ❌ Erro na análise")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def main():
    """Função principal"""
    print("🇦🇴" + "="*40 + "🇦🇴")
    print("   SMARTTOUR ANGOLA - TESTE SIMPLES")
    print("🇦🇴" + "="*40 + "🇦🇴")
    
    tests = [
        ("Arquivos", test_files),
        ("Dependências", test_imports), 
        ("Funcionalidade", test_core)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"\n❌ FALHOU: {name}")
            break
    
    print("\n" + "="*40)
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ SmartTour está funcionando perfeitamente")
    else:
        print(f"⚠️  {passed}/{total} testes passaram")
        print("❌ Corrija os erros antes de usar")
    print("="*40)

if __name__ == "__main__":
    main()
