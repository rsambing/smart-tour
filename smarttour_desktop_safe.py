#!/usr/bin/env python3
"""
SmartTour Angola - Desktop App (Safe Version)
Interface desktop segura para análise de turismo sustentável
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

# Import do sistema SmartTour
try:
    from smarttour_integrated import SmartTourAngola
except ImportError:
    print("❌ Erro: smarttour_integrated.py não encontrado")
    sys.exit(1)

class SmartTourDesktopSafe:
    """Aplicação desktop segura do SmartTour Angola"""
    
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.smarttour = SmartTourAngola()
            self.setup_window()
            self.setup_ui()
            self.add_log("SmartTour Desktop iniciado com sucesso")
        except Exception as e:
            print(f"❌ Erro na inicialização: {e}")
            sys.exit(1)
    
    def setup_window(self):
        """Configura janela principal"""
        self.root.title("🇦🇴 SmartTour Angola - Desktop")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a1a')
        
        # Prevenir fechamento acidental
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Configura interface simples e segura"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header_frame, 
                              text="🇦🇴 SmartTour Angola",
                              bg='#2d2d2d', fg='#ffd700',
                              font=('Arial', 20, 'bold'))
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Sistema de Análise de Turismo Sustentável",
                                 bg='#2d2d2d', fg='#00d084',
                                 font=('Arial', 12))
        subtitle_label.pack(pady=(0, 15))
        
        # Frame de controles
        controls_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        controls_frame.pack(fill='x', pady=(0, 20))
        
        controls_title = tk.Label(controls_frame,
                                 text="🎛️ Controles",
                                 bg='#2d2d2d', fg='#ffd700',
                                 font=('Arial', 14, 'bold'))
        controls_title.pack(pady=(15, 10))
        
        # Botões principais
        buttons_frame = tk.Frame(controls_frame, bg='#2d2d2d')
        buttons_frame.pack(pady=(0, 15))
        
        self.btn_load = tk.Button(buttons_frame,
                                 text="📊 Carregar Dados Padrão",
                                 bg='#00d084', fg='white',
                                 font=('Arial', 11, 'bold'),
                                 command=self.load_default_data,
                                 relief='flat', bd=0,
                                 padx=20, pady=10)
        self.btn_load.pack(side='left', padx=5)
        
        self.btn_custom = tk.Button(buttons_frame,
                                   text="📁 Carregar Personalizados",
                                   bg='#00d084', fg='white',
                                   font=('Arial', 11, 'bold'),
                                   command=self.load_custom_data,
                                   relief='flat', bd=0,
                                   padx=20, pady=10)
        self.btn_custom.pack(side='left', padx=5)
        
        self.btn_analyze = tk.Button(buttons_frame,
                                    text="🔍 Executar Análise",
                                    bg='#ffd700', fg='#1a1a1a',
                                    font=('Arial', 11, 'bold'),
                                    command=self.run_analysis,
                                    relief='flat', bd=0,
                                    padx=20, pady=10)
        self.btn_analyze.pack(side='left', padx=5)
        
        self.btn_export = tk.Button(buttons_frame,
                                   text="📄 Gerar Relatório",
                                   bg='#ffd700', fg='#1a1a1a',
                                   font=('Arial', 11, 'bold'),
                                   command=self.export_report,
                                   relief='flat', bd=0,
                                   padx=20, pady=10)
        self.btn_export.pack(side='left', padx=5)
        
        self.btn_open = tk.Button(buttons_frame,
                                 text="🌐 Abrir Relatório",
                                 bg='#00d084', fg='white',
                                 font=('Arial', 11, 'bold'),
                                 command=self.open_report,
                                 relief='flat', bd=0,
                                 padx=20, pady=10)
        self.btn_open.pack(side='right', padx=5)
        
        # Status simples
        status_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        status_frame.pack(fill='x', pady=(0, 20))
        
        status_title = tk.Label(status_frame,
                               text="📈 Status do Sistema",
                               bg='#2d2d2d', fg='#ffd700',
                               font=('Arial', 14, 'bold'))
        status_title.pack(pady=(15, 10))
        
        # KPIs simples
        self.kpi_frame = tk.Frame(status_frame, bg='#2d2d2d')
        self.kpi_frame.pack(pady=(0, 15))
        
        self.update_kpis()
        
        # Log area
        log_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        log_frame.pack(fill='both', expand=True)
        
        log_title = tk.Label(log_frame,
                            text="📋 Log do Sistema",
                            bg='#2d2d2d', fg='#ffd700',
                            font=('Arial', 14, 'bold'))
        log_title.pack(pady=(15, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 bg='#1a1a1a', fg='#66ff99',
                                                 font=('Consolas', 10),
                                                 wrap='word', height=15)
        self.log_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Log inicial
        self.add_log("Sistema iniciado e pronto para uso")
        self.add_log("Use os botões acima para carregar dados e executar análise")
    
    def update_kpis(self):
        """Atualiza KPIs de forma simples"""
        # Limpar KPIs existentes
        for widget in self.kpi_frame.winfo_children():
            widget.destroy()
        
        status = self.smarttour.get_status()
        
        # KPI simples - dados carregados
        data_status = "✅ Carregado" if status['data_loaded'] else "❌ Não carregado"
        data_color = '#00d084' if status['data_loaded'] else '#CE1126'
        
        data_label = tk.Label(self.kpi_frame,
                             text=f"Dados: {data_status} | Visitantes: {status['visitor_records']} | Sítios: {status['eco_sites_available']}",
                             bg='#2d2d2d', fg=data_color,
                             font=('Arial', 11, 'bold'))
        data_label.pack(pady=5)
        
        # KPI de análise
        analysis_status = "✅ Concluída" if status['analysis_completed'] else "⏳ Pendente"
        analysis_color = '#00d084' if status['analysis_completed'] else '#ffd700'
        
        analysis_label = tk.Label(self.kpi_frame,
                                 text=f"Análise: {analysis_status}",
                                 bg='#2d2d2d', fg=analysis_color,
                                 font=('Arial', 11, 'bold'))
        analysis_label.pack(pady=5)
        
        # Se análise concluída, mostrar KPIs principais
        if status['analysis_completed']:
            try:
                kpis = self.smarttour.kpis
                tourism = kpis.get('tourism_kpis', {})
                sustainability = kpis.get('sustainability_kpis', {})
                
                kpi_text = f"Visitantes Anuais: {tourism.get('total_annual_visitors', 0):,} | "
                kpi_text += f"Sites Sustentáveis: {sustainability.get('sustainable_sites_percentage', 0)}%"
                
                kpi_label = tk.Label(self.kpi_frame,
                                   text=kpi_text,
                                   bg='#2d2d2d', fg='#66ff99',
                                   font=('Arial', 10))
                kpi_label.pack(pady=5)
            except:
                pass
    
    def add_log(self, message):
        """Adiciona mensagem ao log"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            self.log_text.insert('end', log_entry)
            self.log_text.see('end')
            self.root.update_idletasks()
        except:
            pass  # Ignore se der erro no log
    
    def disable_buttons(self):
        """Desabilita botões durante operações"""
        self.btn_load.config(state='disabled')
        self.btn_custom.config(state='disabled')
        self.btn_analyze.config(state='disabled')
        self.btn_export.config(state='disabled')
    
    def enable_buttons(self):
        """Reabilita botões"""
        self.btn_load.config(state='normal')
        self.btn_custom.config(state='normal')
        self.btn_analyze.config(state='normal')
        self.btn_export.config(state='normal')
    
    def load_default_data(self):
        """Carrega dados padrão"""
        try:
            self.add_log("Carregando dados padrão...")
            self.disable_buttons()
            
            success = self.smarttour.load_data()
            
            if success:
                self.add_log("✅ Dados padrão carregados com sucesso!")
                messagebox.showinfo("Sucesso", "Dados padrão carregados!")
            else:
                self.add_log("❌ Erro ao carregar dados padrão")
                messagebox.showerror("Erro", "Erro ao carregar dados padrão")
            
            self.update_kpis()
            
        except Exception as e:
            self.add_log(f"❌ Erro: {e}")
            messagebox.showerror("Erro", f"Erro: {e}")
        finally:
            self.enable_buttons()
    
    def load_custom_data(self):
        """Carrega dados personalizados"""
        try:
            visitors_file = filedialog.askopenfilename(
                title="Selecione arquivo de visitantes",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not visitors_file:
                return
            
            eco_sites_file = filedialog.askopenfilename(
                title="Selecione arquivo de sítios ecológicos",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not eco_sites_file:
                return
            
            self.add_log(f"Carregando dados personalizados...")
            self.add_log(f"Visitantes: {Path(visitors_file).name}")
            self.add_log(f"Sítios: {Path(eco_sites_file).name}")
            self.disable_buttons()
            
            success = self.smarttour.load_data(visitors_file, eco_sites_file)
            
            if success:
                self.add_log("✅ Dados personalizados carregados com sucesso!")
                messagebox.showinfo("Sucesso", "Dados personalizados carregados!")
            else:
                self.add_log("❌ Erro ao carregar dados personalizados")
                messagebox.showerror("Erro", "Erro ao carregar dados personalizados")
            
            self.update_kpis()
            
        except Exception as e:
            self.add_log(f"❌ Erro: {e}")
            messagebox.showerror("Erro", f"Erro: {e}")
        finally:
            self.enable_buttons()
    
    def run_analysis(self):
        """Executa análise"""
        if not self.smarttour.data_loaded:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro!")
            return
        
        try:
            self.add_log("🔍 Iniciando análise completa...")
            self.disable_buttons()
            
            success = self.smarttour.perform_analysis()
            
            if success:
                self.add_log("✅ Análise concluída com sucesso!")
                messagebox.showinfo("Sucesso", "Análise concluída!\n\nKPIs atualizados na interface.")
            else:
                self.add_log("❌ Erro na análise")
                messagebox.showerror("Erro", "Erro na análise")
            
            self.update_kpis()
            
        except Exception as e:
            self.add_log(f"❌ Erro: {e}")
            messagebox.showerror("Erro", f"Erro: {e}")
        finally:
            self.enable_buttons()
    
    def export_report(self):
        """Exporta relatório HTML"""
        if not self.smarttour.analysis_completed:
            messagebox.showwarning("Aviso", "Execute a análise primeiro!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                title="Salvar relatório como..."
            )
            
            if not filename:
                return
            
            self.add_log(f"📄 Gerando relatório: {Path(filename).name}")
            self.disable_buttons()
            
            success = self.smarttour.export_report(filename)
            
            if success:
                self.add_log(f"✅ Relatório salvo: {filename}")
                result = messagebox.askyesno("Sucesso", 
                                           f"Relatório salvo em:\n{filename}\n\nDeseja abrir agora?")
                if result:
                    webbrowser.open(f"file://{os.path.abspath(filename)}")
            else:
                self.add_log("❌ Erro ao gerar relatório")
                messagebox.showerror("Erro", "Erro ao gerar relatório")
            
        except Exception as e:
            self.add_log(f"❌ Erro: {e}")
            messagebox.showerror("Erro", f"Erro: {e}")
        finally:
            self.enable_buttons()
    
    def open_report(self):
        """Abre relatório existente"""
        try:
            # Procurar arquivo padrão
            default_path = "smarttour_angola_report.html"
            if os.path.exists(default_path):
                webbrowser.open(f"file://{os.path.abspath(default_path)}")
                self.add_log(f"🌐 Relatório aberto: {default_path}")
            else:
                # Permitir selecionar arquivo
                filename = filedialog.askopenfilename(
                    title="Selecione relatório para abrir",
                    filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
                )
                if filename:
                    webbrowser.open(f"file://{os.path.abspath(filename)}")
                    self.add_log(f"🌐 Relatório aberto: {Path(filename).name}")
                else:
                    messagebox.showinfo("Info", "Gere um relatório primeiro!")
        except Exception as e:
            self.add_log(f"❌ Erro ao abrir relatório: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir relatório: {e}")
    
    def on_closing(self):
        """Confirma fechamento"""
        if messagebox.askokcancel("Sair", "Deseja sair do SmartTour Angola?"):
            self.add_log("👋 Encerrando aplicação...")
            self.root.destroy()
    
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.add_log("Aplicação interrompida pelo usuário")
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")

def main():
    """Função principal com tratamento de erro"""
    try:
        # Verificar se há display disponível
        try:
            import tkinter
            root_test = tkinter.Tk()
            root_test.destroy()
        except Exception as e:
            print("❌ Erro: Interface gráfica não disponível")
            print(f"Detalhes: {e}")
            print("\n💡 Alternativas:")
            print("1. Use a interface web: python3 smarttour_web.py")
            print("2. Use o modo terminal: python3 smarttour_integrated.py")
            return
        
        print("🖥️ Iniciando SmartTour Angola Desktop (Safe Mode)")
        app = SmartTourDesktopSafe()
        app.run()
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        print("\n💡 Alternativas:")
        print("1. Use a interface web: python3 smarttour_web.py")
        print("2. Use o modo terminal: python3 smarttour_integrated.py")

if __name__ == "__main__":
    main()
