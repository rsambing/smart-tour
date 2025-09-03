
# Interface Desktop Minimalista para SmartTour Angola
# Mantém apenas funções essenciais e comentários em português simples

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

# Importa a lógica principal do SmartTour
try:
    from smarttour_integrated import SmartTourAngola
except ImportError:
    print("Erro: smarttour_integrated.py não encontrado")
    sys.exit(1)


class SmartTourDesktopMinimal:
    """
    Interface desktop minimalista do SmartTour Angola
    Comentários em português simples
    """
    def __init__(self):
        # Inicializa janela principal
        self.root = tk.Tk()
        self.root.title("SmartTour Angola - Desktop Minimalista")
        self.root.geometry("600x400")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Instancia o sistema principal
        self.smarttour = SmartTourAngola()

        # Área de botões
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Botão para carregar dados padrão
        self.btn_load = tk.Button(frame, text="Carregar Dados Padrão", command=self.load_default_data)
        self.btn_load.pack(side='left', padx=5)

        # Botão para carregar dados personalizados
        self.btn_custom = tk.Button(frame, text="Carregar Dados Personalizados", command=self.load_custom_data)
        self.btn_custom.pack(side='left', padx=5)

        # Botão para executar análise
        self.btn_analyze = tk.Button(frame, text="Executar Análise", command=self.run_analysis)
        self.btn_analyze.pack(side='left', padx=5)

        # Botão para exportar relatório
        self.btn_export = tk.Button(frame, text="Exportar Relatório", command=self.export_report)
        self.btn_export.pack(side='left', padx=5)

        # Botão para abrir relatório
        self.btn_open = tk.Button(frame, text="Abrir Relatório", command=self.open_report)
        self.btn_open.pack(side='left', padx=5)

        # Área de log para mensagens
        self.log_text = scrolledtext.ScrolledText(self.root, height=10)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)

        # Área de status simples
        self.status_label = tk.Label(self.root, text="Status: Pronto", fg="green")
        self.status_label.pack(pady=5)

        self.add_log("Sistema iniciado. Use os botões acima.")

    def add_log(self, msg):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {msg}\n")
        self.log_text.see('end')

    def update_status(self, msg, color="black"):
        """Atualiza status na interface"""
        self.status_label.config(text=f"Status: {msg}", fg=color)

    def load_default_data(self):
        """Carrega dados padrão do sistema"""
        self.add_log("Carregando dados padrão...")
        ok = self.smarttour.load_data()
        if ok:
            self.add_log("Dados padrão carregados com sucesso!")
            self.update_status("Dados carregados", "green")
        else:
            self.add_log("Erro ao carregar dados padrão.")
            self.update_status("Erro ao carregar dados", "red")

    def load_custom_data(self):
        """Carrega dados personalizados (visitantes e sítios)"""
        visitantes = filedialog.askopenfilename(title="Arquivo de visitantes", filetypes=[("CSV", "*.csv")])
        if not visitantes:
            return
        sitios = filedialog.askopenfilename(title="Arquivo de sítios ecológicos", filetypes=[("CSV", "*.csv")])
        if not sitios:
            return
        self.add_log(f"Carregando visitantes: {visitantes}")
        self.add_log(f"Carregando sítios: {sitios}")
        ok = self.smarttour.load_data(visitantes, sitios)
        if ok:
            self.add_log("Dados personalizados carregados!")
            self.update_status("Dados carregados", "green")
        else:
            self.add_log("Erro ao carregar dados personalizados.")
            self.update_status("Erro ao carregar dados", "red")

    def run_analysis(self):
        """Executa análise dos dados"""
        if not getattr(self.smarttour, 'data_loaded', False):
            self.add_log("Carregue os dados antes de analisar.")
            self.update_status("Dados não carregados", "red")
            return
        self.add_log("Executando análise...")
        ok = self.smarttour.perform_analysis()
        if ok:
            self.add_log("Análise concluída!")
            self.update_status("Análise concluída", "green")
        else:
            self.add_log("Erro na análise.")
            self.update_status("Erro na análise", "red")

    def export_report(self):
        """Exporta relatório HTML"""
        if not getattr(self.smarttour, 'analysis_completed', False):
            self.add_log("Execute a análise antes de exportar.")
            self.update_status("Análise não concluída", "red")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML", "*.html")])
        if not filename:
            return
        self.add_log(f"Exportando relatório: {filename}")
        ok = self.smarttour.export_report(filename)
        if ok:
            self.add_log("Relatório exportado!")
            self.update_status("Relatório exportado", "green")
        else:
            self.add_log("Erro ao exportar relatório.")
            self.update_status("Erro ao exportar relatório", "red")

    def open_report(self):
        """Abre relatório HTML gerado"""
        default_path = "smarttour_angola_report.html"
        if os.path.exists(default_path):
            webbrowser.open(f"file://{os.path.abspath(default_path)}")
            self.add_log(f"Relatório aberto: {default_path}")
        else:
            filename = filedialog.askopenfilename(title="Abrir relatório", filetypes=[("HTML", "*.html")])
            if filename:
                webbrowser.open(f"file://{os.path.abspath(filename)}")
                self.add_log(f"Relatório aberto: {filename}")

    def on_closing(self):
        """Confirma fechamento da aplicação"""
        if messagebox.askokcancel("Sair", "Deseja sair?"):
            self.add_log("Encerrando aplicação...")
            self.root.destroy()

    def run(self):
        """Executa a interface desktop"""
        self.root.mainloop()
    
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


# Função principal: executa a interface desktop minimalista
def main():
    try:
        app = SmartTourDesktopMinimal()
        app.run()
    except Exception as e:
        print(f"Erro fatal: {e}")
        print("Alternativas:")
        print("1. python3 smarttour_web.py (interface web)")
        print("2. python3 smarttour_integrated.py (terminal)")

if __name__ == "__main__":
    main()
