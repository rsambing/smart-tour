#!/usr/bin/env python3
"""
SmartTour Angola - Interface Desktop Simplificada
Versão minimalista e funcional usando o núcleo unificado
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import webbrowser
import os
from datetime import datetime
from pathlib import Path
import sys

# Importa o núcleo simplificado
try:
    from smarttour_core import SmartTourCore
except ImportError:
    print("❌ Erro: smarttour_core.py não encontrado")
    sys.exit(1)


class SmartTourDesktop:
    """Interface desktop simples do SmartTour Angola"""
    
    def __init__(self):
        # Cria janela principal
        self.root = tk.Tk()
        self.root.title("SmartTour Angola - Desktop")
        self.root.geometry("700x500")
        self.root.configure(bg='#f5f5f5')
        
        # Inicializa o núcleo do SmartTour
        self.smarttour = SmartTourCore()
        
        # Cria interface
        self.create_interface()
        
        # Configura fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.log("Sistema pronto. Use os botões para começar.")
    
    def create_interface(self):
        """Cria interface simples e funcional"""
        
        # Cabeçalho
        header = tk.Frame(self.root, bg='#CE1126', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🇦🇴 SmartTour Angola", 
                        font=('Arial', 16, 'bold'),
                        bg='#CE1126', fg='white')
        title.pack(pady=15)
        
        # Status
        self.status_frame = tk.Frame(self.root, bg='#e9ecef', height=40)
        self.status_frame.pack(fill='x')
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame, 
                                   text="Status: Pronto", 
                                   bg='#e9ecef', fg='#28a745',
                                   font=('Arial', 10, 'bold'))
        self.status_label.pack(pady=10)
        
        # Botões
        button_frame = tk.Frame(self.root, bg='#f5f5f5')
        button_frame.pack(fill='x', padx=20, pady=10)
        
        # Define botões principais
        self.btn_load = tk.Button(button_frame, text="Carregar Dados", 
                                 command=self.load_data, bg='#28a745', fg='white',
                                 font=('Arial', 10, 'bold'), width=15, height=2)
        self.btn_load.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_analyze = tk.Button(button_frame, text="Executar Análise", 
                                    command=self.analyze_data, bg='#ffc107', fg='black',
                                    font=('Arial', 10, 'bold'), width=15, height=2)
        self.btn_analyze.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_export = tk.Button(button_frame, text="Gerar Relatório", 
                                   command=self.export_report, bg='#17a2b8', fg='white',
                                   font=('Arial', 10, 'bold'), width=15, height=2)
        self.btn_export.grid(row=1, column=0, padx=5, pady=5)
        
        self.btn_open = tk.Button(button_frame, text="Abrir Relatório", 
                                 command=self.open_report, bg='#fd7e14', fg='white',
                                 font=('Arial', 10, 'bold'), width=15, height=2)
        self.btn_open.grid(row=1, column=1, padx=5, pady=5)
        
        # Log
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Log de Atividades:", 
                font=('Arial', 10, 'bold')).pack(anchor='w')
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15,
                                                font=('Courier', 9),
                                                bg='#2d3748', fg='#e2e8f0')
        self.log_text.pack(fill='both', expand=True, pady=(5,0))
    
    def log(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}\n"
        self.log_text.insert('end', entry)
        self.log_text.see('end')
        self.root.update_idletasks()
    
    def update_status(self, message, color='#28a745'):
        """Atualiza status"""
        self.status_label.config(text=f"Status: {message}", fg=color)
    
    def load_data(self):
        """Carrega dados padrão ou personalizados"""
        # Pergunta se quer usar dados padrão ou personalizar
        use_default = messagebox.askyesno("Carregar Dados", 
                                         "Usar dados padrão?\n\n"
                                         "Sim = Dados padrão\n"
                                         "Não = Escolher arquivos")
        
        if use_default:
            self.log("Carregando dados padrão...")
            success = self.smarttour.load_data()
        else:
            # Seleciona arquivos personalizados
            visitors_file = filedialog.askopenfilename(
                title="Selecione arquivo de visitantes",
                filetypes=[("CSV files", "*.csv")]
            )
            if not visitors_file:
                return
            
            sites_file = filedialog.askopenfilename(
                title="Selecione arquivo de sítios ecológicos", 
                filetypes=[("CSV files", "*.csv")]
            )
            if not sites_file:
                return
            
            self.log(f"Carregando arquivos personalizados...")
            self.log(f"Visitantes: {Path(visitors_file).name}")
            self.log(f"Sítios: {Path(sites_file).name}")
            success = self.smarttour.load_data(visitors_file, sites_file)
        
        if success:
            status = self.smarttour.get_status()
            self.log("✅ Dados carregados com sucesso!")
            self.log(f"   • Visitantes: {status['visitor_records']} registros")
            self.log(f"   • Sítios: {status['eco_sites_available']} registros")
            self.log(f"   • Províncias: {status['provinces_available']}")
            self.update_status("Dados carregados", '#28a745')
        else:
            self.log("❌ Erro ao carregar dados")
            self.update_status("Erro ao carregar", '#dc3545')
    
    def analyze_data(self):
        """Executa análise dos dados"""
        if not self.smarttour.data_loaded:
            self.log("❌ Carregue os dados primeiro")
            messagebox.showwarning("Aviso", "Carregue os dados primeiro!")
            return
        
        self.log("🔍 Executando análise...")
        self.update_status("Analisando...", '#ffc107')
        
        success = self.smarttour.perform_analysis()
        
        if success:
            self.log("✅ Análise concluída com sucesso!")
            
            # Mostra KPIs principais
            kpis = self.smarttour.kpis
            tourism = kpis.get('tourism', {})
            sustainability = kpis.get('sustainability', {})
            
            self.log("📊 Resultados principais:")
            self.log(f"   • Visitantes anuais: {tourism.get('annual_visitors', 0):,}")
            self.log(f"   • Sites sustentáveis: {sustainability.get('sustainable_percentage', 0)}%")
            self.log(f"   • Score sustentabilidade: {sustainability.get('sustainability_score', 0):.1f}/10")
            
            self.update_status("Análise concluída", '#28a745')
            messagebox.showinfo("Sucesso", "Análise concluída!")
        else:
            self.log("❌ Erro na análise")
            self.update_status("Erro na análise", '#dc3545')
            messagebox.showerror("Erro", "Erro na análise")
    
    def export_report(self):
        """Exporta relatório HTML"""
        if not self.smarttour.analysis_completed:
            self.log("❌ Execute a análise primeiro")
            messagebox.showwarning("Aviso", "Execute a análise primeiro!")
            return
        
        # Pergunta onde salvar
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html")],
            title="Salvar relatório como..."
        )
        
        if not filename:
            return
        
        self.log(f"📄 Gerando relatório: {Path(filename).name}")
        self.update_status("Gerando relatório...", '#ffc107')
        
        success = self.smarttour.export_report(filename)
        
        if success:
            self.log(f"✅ Relatório salvo: {filename}")
            self.update_status("Relatório gerado", '#28a745')
            
            # Pergunta se quer abrir
            if messagebox.askyesno("Sucesso", 
                                  f"Relatório salvo!\n\nDeseja abrir agora?"):
                webbrowser.open(f"file://{os.path.abspath(filename)}")
        else:
            self.log("❌ Erro ao gerar relatório")
            self.update_status("Erro ao gerar", '#dc3545')
            messagebox.showerror("Erro", "Erro ao gerar relatório")
    
    def open_report(self):
        """Abre relatório existente"""
        # Tenta arquivo padrão primeiro
        default_file = "smarttour_angola_report.html"
        
        if os.path.exists(default_file):
            webbrowser.open(f"file://{os.path.abspath(default_file)}")
            self.log(f"🌐 Relatório aberto: {default_file}")
        else:
            # Permite selecionar arquivo
            filename = filedialog.askopenfilename(
                title="Selecione relatório para abrir",
                filetypes=[("HTML files", "*.html")]
            )
            
            if filename:
                webbrowser.open(f"file://{os.path.abspath(filename)}")
                self.log(f"🌐 Relatório aberto: {Path(filename).name}")
            else:
                messagebox.showinfo("Info", "Gere um relatório primeiro!")
    
    def on_close(self):
        """Confirma fechamento"""
        if messagebox.askokcancel("Sair", "Deseja sair do SmartTour Angola?"):
            self.log("👋 Encerrando aplicação...")
            self.root.destroy()
    
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()


def main():
    """Função principal"""
    try:
        # Verifica se tkinter está disponível
        root_test = tk.Tk()
        root_test.destroy()
        
        # Inicia aplicação
        app = SmartTourDesktop()
        app.run()
        
    except Exception as e:
        print(f"❌ Erro na interface desktop: {e}")
        print("💡 Alternativas:")
        print("   python3 smarttour_web.py (interface web)")
        print("   python3 smarttour_integrated.py (terminal)")


if __name__ == "__main__":
    main()
