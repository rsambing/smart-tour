#!/usr/bin/env python3
"""
SmartTour Angola - Desktop App
Interface desktop moderna para análise de turismo sustentável
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
from pathlib import Path
import threading
import webbrowser
import os
from datetime import datetime

# Import do sistema SmartTour
from smarttour_integrated import SmartTourAngola

class SmartTourDesktop:
    """Aplicação desktop do SmartTour Angola"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.smarttour = SmartTourAngola()
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Configura tema escuro moderno com verde e dourado"""
        
        # Cores do tema ecológico
        self.colors = {
            'bg_dark': '#1a1a1a',        # Fundo escuro principal
            'bg_medium': '#2d2d2d',      # Fundo médio
            'bg_light': '#404040',       # Fundo claro
            'green_primary': '#00d084',   # Verde principal (moderno)
            'green_secondary': '#66ff99', # Verde claro
            'gold': '#ffd700',           # Dourado
            'gold_light': '#ffed4e',     # Dourado claro
            'white': '#ffffff',          # Branco
            'gray': '#cccccc',           # Cinza claro
            'red_angola': '#CE1126',     # Vermelho Angola
            'yellow_angola': '#FFCD00'   # Amarelo Angola
        }
        
        # Configuração da janela principal
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Estilo para ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurações de estilo
        self.style.configure('Dark.TFrame', background=self.colors['bg_dark'])
        self.style.configure('Medium.TFrame', background=self.colors['bg_medium'])
        
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_dark'],
                           foreground=self.colors['gold'],
                           font=('Segoe UI', 24, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['bg_dark'],
                           foreground=self.colors['green_primary'],
                           font=('Segoe UI', 14, 'bold'))
        
        self.style.configure('Info.TLabel',
                           background=self.colors['bg_dark'],
                           foreground=self.colors['white'],
                           font=('Segoe UI', 10))
        
        self.style.configure('Green.TButton',
                           background=self.colors['green_primary'],
                           foreground='white',
                           font=('Segoe UI', 11, 'bold'),
                           borderwidth=0,
                           focuscolor='none')
        
        self.style.configure('Gold.TButton',
                           background=self.colors['gold'],
                           foreground=self.colors['bg_dark'],
                           font=('Segoe UI', 11, 'bold'),
                           borderwidth=0,
                           focuscolor='none')
    
    def setup_ui(self):
        """Configura interface do usuário"""
        
        self.root.title("🇦🇴 SmartTour Angola - Desktop")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Ícone da janela (usar emoji como fallback)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Cabeçalho
        self.create_header()
        
        # Área de controles
        self.create_controls()
        
        # Área de resultados
        self.create_results_area()
        
        # Área de status
        self.create_status_bar()
    
    def create_header(self):
        """Cria cabeçalho da aplicação"""
        
        header_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Título principal
        title = ttk.Label(header_frame, text="🇦🇴 SmartTour Angola", style='Title.TLabel')
        title.pack(anchor='w')
        
        # Subtítulo
        subtitle = ttk.Label(header_frame, 
                           text="Sistema de Análise de Turismo Sustentável", 
                           style='Subtitle.TLabel')
        subtitle.pack(anchor='w')
        
        # Info adicional
        info = ttk.Label(header_frame,
                        text="Descentralização e Ecoturismo | FTL Bootcamp",
                        style='Info.TLabel')
        info.pack(anchor='w', pady=(5, 0))
    
    def create_controls(self):
        """Cria área de controles"""
        
        controls_frame = ttk.LabelFrame(self.main_frame, text="🎛️ Controles", 
                                      style='Medium.TFrame', padding=15)
        controls_frame.pack(fill='x', pady=(0, 20))
        
        # Frame para botões
        buttons_frame = ttk.Frame(controls_frame, style='Medium.TFrame')
        buttons_frame.pack(fill='x')
        
        # Botões principais
        btn_load_default = ttk.Button(buttons_frame, 
                                    text="📊 Carregar Dados Padrão",
                                    style='Green.TButton',
                                    command=self.load_default_data)
        btn_load_default.pack(side='left', padx=(0, 10))
        
        btn_load_custom = ttk.Button(buttons_frame,
                                   text="📁 Carregar Arquivos Personalizados", 
                                   style='Green.TButton',
                                   command=self.load_custom_data)
        btn_load_custom.pack(side='left', padx=(0, 10))
        
        btn_analyze = ttk.Button(buttons_frame,
                               text="🔍 Executar Análise",
                               style='Gold.TButton', 
                               command=self.run_analysis)
        btn_analyze.pack(side='left', padx=(0, 10))
        
        btn_export = ttk.Button(buttons_frame,
                              text="📄 Gerar Relatório HTML",
                              style='Gold.TButton',
                              command=self.export_report)
        btn_export.pack(side='left', padx=(0, 10))
        
        btn_open_report = ttk.Button(buttons_frame,
                                   text="🌐 Abrir Relatório",
                                   style='Green.TButton',
                                   command=self.open_report)
        btn_open_report.pack(side='right')
    
    def create_results_area(self):
        """Cria área de resultados"""
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, pady=(0, 10))
        
        # Aba 1: KPIs Principais
        self.create_kpis_tab()
        
        # Aba 2: Dados Detalhados
        self.create_data_tab()
        
        # Aba 3: Log do Sistema
        self.create_log_tab()
    
    def create_kpis_tab(self):
        """Cria aba de KPIs principais"""
        
        kpis_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(kpis_frame, text="📈 KPIs Principais")
        
        # Frame para cartões de KPI
        cards_frame = ttk.Frame(kpis_frame, style='Dark.TFrame')
        cards_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Grid de KPIs
        self.create_kpi_cards(cards_frame)
    
    def create_kpi_cards(self, parent):
        """Cria cartões de KPI"""
        
        # Frame para linha 1
        row1 = ttk.Frame(parent, style='Dark.TFrame')
        row1.pack(fill='x', pady=(0, 20))
        
        # Frame para linha 2
        row2 = ttk.Frame(parent, style='Dark.TFrame')
        row2.pack(fill='x')
        
        # KPI Cards
        self.kpi_cards = {}
        
        # Linha 1 - KPIs de Turismo
        self.kpi_cards['visitors'] = self.create_kpi_card(row1, "👥 Visitantes Anuais", "0", self.colors['green_primary'])
        self.kpi_cards['foreign'] = self.create_kpi_card(row1, "🌍 Visitantes Estrangeiros", "0%", self.colors['gold'])
        self.kpi_cards['stay'] = self.create_kpi_card(row1, "🏨 Estadia Média", "0 noites", self.colors['green_secondary'])
        
        # Linha 2 - KPIs de Sustentabilidade  
        self.kpi_cards['sustainable'] = self.create_kpi_card(row2, "🌱 Sites Sustentáveis", "0%", self.colors['green_primary'])
        self.kpi_cards['capacity'] = self.create_kpi_card(row2, "🏞️ Capacidade Total", "0/dia", self.colors['gold'])
        self.kpi_cards['score'] = self.create_kpi_card(row2, "⭐ Score Sustentabilidade", "0/10", self.colors['green_secondary'])
    
    def create_kpi_card(self, parent, title, value, color):
        """Cria um cartão individual de KPI"""
        
        card_frame = tk.Frame(parent, bg=self.colors['bg_medium'], 
                            relief='raised', bd=2)
        
        # Determinar padding baseado na posição
        existing_children = len(parent.winfo_children())
        padx = (0, 10) if existing_children < 2 else (0, 0)
        card_frame.pack(side='left', fill='both', expand=True, padx=padx)
        
        # Título
        title_label = tk.Label(card_frame, text=title,
                             bg=self.colors['bg_medium'],
                             fg=self.colors['gray'],
                             font=('Segoe UI', 10))
        title_label.pack(pady=(15, 5))
        
        # Valor
        value_label = tk.Label(card_frame, text=value,
                             bg=self.colors['bg_medium'],
                             fg=color,
                             font=('Segoe UI', 18, 'bold'))
        value_label.pack(pady=(0, 15))
        
        return value_label
    
    def create_data_tab(self):
        """Cria aba de dados detalhados"""
        
        data_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(data_frame, text="📊 Dados Detalhados")
        
        # Área de texto com scroll
        self.data_text = scrolledtext.ScrolledText(
            data_frame,
            bg=self.colors['bg_medium'],
            fg=self.colors['white'],
            font=('Consolas', 10),
            wrap='word',
            height=25
        )
        self.data_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Texto inicial
        self.data_text.insert('1.0', 
            "🇦🇴 SmartTour Angola - Dados Detalhados\n" +
            "=" * 60 + "\n\n" +
            "Carregue os dados para visualizar informações detalhadas...\n\n" +
            "📊 Funcionalidades disponíveis:\n" +
            "• Análise de visitantes por província\n" +
            "• Avaliação de sustentabilidade de sítios\n" +
            "• KPIs automatizados\n" +
            "• Relatórios HTML interativos\n\n"
        )
    
    def create_log_tab(self):
        """Cria aba de log do sistema"""
        
        log_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(log_frame, text="📋 Log do Sistema")
        
        # Área de log
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            bg=self.colors['bg_dark'],
            fg=self.colors['green_secondary'],
            font=('Consolas', 9),
            wrap='word',
            height=25
        )
        self.log_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Log inicial
        self.add_log("SmartTour Angola Desktop iniciado")
        self.add_log("Sistema pronto para carregar dados")
    
    def create_status_bar(self):
        """Cria barra de status"""
        
        self.status_frame = ttk.Frame(self.main_frame, style='Medium.TFrame')
        self.status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame,
                                    text="🟢 Sistema pronto",
                                    style='Info.TLabel')
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Indicador de progresso
        self.progress = ttk.Progressbar(self.status_frame, mode='indeterminate')
        self.progress.pack(side='right', padx=10, pady=5)
    
    def add_log(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert('end', log_entry)
        self.log_text.see('end')
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Atualiza barra de status"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def show_progress(self, show=True):
        """Mostra/esconde barra de progresso"""
        if show:
            self.progress.start(10)
        else:
            self.progress.stop()
    
    def load_default_data(self):
        """Carrega dados padrão do hackathon"""
        self.add_log("Iniciando carregamento de dados padrão...")
        self.update_status("🔄 Carregando dados padrão...")
        self.show_progress(True)
        
        def load_task():
            try:
                success = self.smarttour.load_data()
                
                if success:
                    self.root.after(0, lambda: self.on_data_loaded(True, "Dados padrão carregados com sucesso!"))
                else:
                    self.root.after(0, lambda: self.on_data_loaded(False, "Erro ao carregar dados padrão"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_data_loaded(False, f"Erro: {str(e)}"))
        
        # Executar em thread separada
        threading.Thread(target=load_task, daemon=True).start()
    
    def load_custom_data(self):
        """Carrega dados personalizados"""
        
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
        
        self.update_status("🔄 Carregando dados personalizados...")
        self.show_progress(True)
        
        def load_task():
            try:
                success = self.smarttour.load_data(visitors_file, eco_sites_file)
                
                if success:
                    message = "Dados personalizados carregados com sucesso!"
                    self.root.after(0, lambda: self.on_data_loaded(True, message))
                else:
                    message = "Erro ao carregar dados personalizados"
                    self.root.after(0, lambda: self.on_data_loaded(False, message))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_data_loaded(False, f"Erro: {str(e)}"))
        
        threading.Thread(target=load_task, daemon=True).start()
    
    def on_data_loaded(self, success, message):
        """Callback quando dados são carregados"""
        self.show_progress(False)
        
        if success:
            self.add_log(message)
            self.update_status("🟢 Dados carregados - Pronto para análise")
            
            # Atualizar área de dados
            self.update_data_display()
            
            messagebox.showinfo("Sucesso", message)
        else:
            self.add_log(f"ERRO: {message}")
            self.update_status("🔴 Erro no carregamento")
            messagebox.showerror("Erro", message)
    
    def update_data_display(self):
        """Atualiza exibição de dados"""
        status = self.smarttour.get_status()
        
        data_info = f"""🇦🇴 SmartTour Angola - Dados Carregados
{"=" * 60}

📊 ESTATÍSTICAS DOS DADOS:
• Províncias disponíveis: {status['provinces_available']}
• Sítios ecológicos: {status['eco_sites_available']}
• Status: {'✅ Carregado' if status['data_loaded'] else '❌ Não carregado'}

📋 DADOS DE VISITANTES:
"""
        
        if self.smarttour.visitor_data is not None:
            df = self.smarttour.visitor_data
            data_info += f"""• Total de registros: {len(df)}
• Período: {df['date'].min().strftime('%Y-%m-%d')} até {df['date'].max().strftime('%Y-%m-%d')}
• Províncias: {', '.join(df['province'].unique())}

"""
        
        data_info += "🏞️ DADOS DE SÍTIOS ECOLÓGICOS:\n"
        
        if self.smarttour.eco_sites_data is not None:
            df = self.smarttour.eco_sites_data
            data_info += f"""• Total de sítios: {len(df)}
• Províncias cobertas: {', '.join(df['province'].unique())}
• Capacidade total: {df['capacity_daily'].sum():,} visitantes/dia
• Sítios por fragilidade:
"""
            fragility_counts = df['fragility_index'].value_counts().sort_index()
            for idx, count in fragility_counts.items():
                level = ["", "Muito Baixa", "Baixa", "Média", "Alta", "Muito Alta"][idx]
                data_info += f"  - Índice {idx} ({level}): {count} sítios\n"
        
        data_info += f"""

🔍 PRÓXIMOS PASSOS:
1. Clique em "🔍 Executar Análise" para processar os dados
2. Após a análise, clique em "📄 Gerar Relatório HTML"
3. Use "🌐 Abrir Relatório" para visualizar os resultados

⏰ Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
        
        # Limpa e atualiza texto
        self.data_text.delete('1.0', 'end')
        self.data_text.insert('1.0', data_info)
    
    def run_analysis(self):
        """Executa análise completa"""
        if not self.smarttour.data_loaded:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro!")
            return
        
        self.add_log("Iniciando análise completa...")
        self.update_status("🔄 Executando análise...")
        self.show_progress(True)
        
        def analysis_task():
            try:
                success = self.smarttour.perform_analysis()
                
                if success:
                    self.root.after(0, lambda: self.on_analysis_completed(True, "Análise concluída com sucesso!"))
                else:
                    self.root.after(0, lambda: self.on_analysis_completed(False, "Erro na análise"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_analysis_completed(False, f"Erro: {str(e)}"))
        
        threading.Thread(target=analysis_task, daemon=True).start()
    
    def on_analysis_completed(self, success, message):
        """Callback quando análise é concluída"""
        self.show_progress(False)
        
        if success:
            self.add_log(message)
            self.update_status("🟢 Análise concluída - Pronto para gerar relatório")
            
            # Atualizar KPIs
            self.update_kpi_display()
            
            # Atualizar dados detalhados
            self.update_detailed_results()
            
            messagebox.showinfo("Sucesso", message + "\n\nKPIs atualizados na interface!")
        else:
            self.add_log(f"ERRO: {message}")
            self.update_status("🔴 Erro na análise")
            messagebox.showerror("Erro", message)
    
    def update_kpi_display(self):
        """Atualiza exibição dos KPIs"""
        if not self.smarttour.analysis_completed:
            return
        
        kpis = self.smarttour.kpis
        tourism_kpis = kpis.get('tourism_kpis', {})
        sustainability_kpis = kpis.get('sustainability_kpis', {})
        
        # Atualizar valores dos KPIs
        self.kpi_cards['visitors'].config(text=f"{tourism_kpis.get('total_annual_visitors', 0):,}")
        self.kpi_cards['foreign'].config(text=f"{tourism_kpis.get('foreign_visitor_percentage', 0)}%")
        self.kpi_cards['stay'].config(text=f"{tourism_kpis.get('average_stay_duration', 0)} noites")
        
        self.kpi_cards['sustainable'].config(text=f"{sustainability_kpis.get('sustainable_sites_percentage', 0)}%")
        self.kpi_cards['capacity'].config(text=f"{sustainability_kpis.get('total_eco_capacity', 0):,}/dia")
        self.kpi_cards['score'].config(text=f"{sustainability_kpis.get('average_sustainability_score', 0):.1f}/10")
        
        self.add_log("KPIs atualizados na interface")
    
    def update_detailed_results(self):
        """Atualiza resultados detalhados"""
        if not self.smarttour.analysis_completed:
            return
        
        # Gerar texto detalhado dos resultados
        results_text = self.generate_detailed_results_text()
        
        # Atualizar aba de dados
        self.data_text.delete('1.0', 'end')
        self.data_text.insert('1.0', results_text)
    
    def generate_detailed_results_text(self):
        """Gera texto detalhado dos resultados"""
        kpis = self.smarttour.kpis
        visitor_insights = self.smarttour.visitor_insights
        eco_insights = self.smarttour.eco_insights
        summary = self.smarttour.summary_report
        
        text = f"""🇦🇴 SmartTour Angola - Resultados da Análise
{"=" * 70}

📊 KPIs PRINCIPAIS:
{"─" * 50}

🎯 TURISMO:
• Visitantes anuais estimados: {kpis.get('tourism_kpis', {}).get('total_annual_visitors', 0):,}
• Visitantes estrangeiros: {kpis.get('tourism_kpis', {}).get('foreign_visitor_percentage', 0)}%
• Estadia média: {kpis.get('tourism_kpis', {}).get('average_stay_duration', 0)} noites
• Variação sazonal: {kpis.get('tourism_kpis', {}).get('seasonal_variation', 0)}%

🌱 SUSTENTABILIDADE:
• Sites sustentáveis: {kpis.get('sustainability_kpis', {}).get('sustainable_sites_percentage', 0)}%
• Capacidade total diária: {kpis.get('sustainability_kpis', {}).get('total_eco_capacity', 0):,}
• Score médio de sustentabilidade: {kpis.get('sustainability_kpis', {}).get('average_sustainability_score', 0):.1f}/10
• Províncias com sítios: {kpis.get('sustainability_kpis', {}).get('provinces_with_eco_sites', 0)}

💰 ECONÔMICO:
• Receita anual estimada: {kpis.get('economic_kpis', {}).get('estimated_annual_revenue', 0):,} AOA
• Taxa média por sítio: {kpis.get('economic_kpis', {}).get('average_site_fee', 0):,.0f} AOA

🏆 TOP PROVÍNCIAS POR VISITANTES:
{"─" * 50}
"""
        
        # Top províncias
        if 'top_provinces' in summary:
            for i, (province, data) in enumerate(summary['top_provinces'].items(), 1):
                text += f"{i}. {province}:\n"
                text += f"   • Visitantes: {data['visitors']:,}\n"
                text += f"   • Estrangeiros: {data['foreign_share']}%\n"
                text += f"   • Estadia média: {data['avg_stay']:.1f} noites\n\n"
        
        # Principais achados
        text += f"""💡 PRINCIPAIS ACHADOS:
{"─" * 50}
"""
        if 'executive_summary' in summary:
            for finding in summary['executive_summary'].get('key_findings', []):
                text += f"• {finding}\n"
        
        text += f"""
🎯 RECOMENDAÇÕES:
{"─" * 50}
"""
        if 'executive_summary' in summary:
            for rec in summary['executive_summary'].get('recommendations', []):
                text += f"• {rec}\n"
        
        text += f"""
📈 ANÁLISE SAZONAL:
{"─" * 50}
"""
        if 'seasonal_patterns' in visitor_insights:
            seasonal = visitor_insights['seasonal_patterns']
            text += f"• Época Alta: {seasonal['peak_season']['total_visitors']:,} visitantes\n"
            text += f"• Época Baixa: {seasonal['offpeak_season']['total_visitors']:,} visitantes\n"
        
        text += f"""
🏞️ SÍTIOS POR SUSTENTABILIDADE:
{"─" * 50}
"""
        if 'sustainability_analysis' in eco_insights:
            sustain = eco_insights['sustainability_analysis']
            text += f"• Alta sustentabilidade: {sustain.get('high_sustainability', 0)} sítios\n"
            text += f"• Sustentabilidade moderada: {sustain.get('moderate_sustainability', 0)} sítios\n"
            text += f"• Requer cuidados: {sustain.get('requires_care', 0)} sítios\n"
            text += f"• Alta fragilidade: {sustain.get('high_fragility', 0)} sítios\n"
        
        text += f"""

⏰ Análise gerada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
📋 Use o botão "Gerar Relatório HTML" para obter visualizações interativas!
"""
        
        return text
    
    def export_report(self):
        """Exporta relatório HTML"""
        if not self.smarttour.analysis_completed:
            messagebox.showwarning("Aviso", "Execute a análise primeiro!")
            return
        
        # Selecionar local para salvar
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            title="Salvar relatório como..."
        )
        
        if not filename:
            return
        
        self.add_log(f"Gerando relatório HTML: {Path(filename).name}")
        self.update_status("🔄 Gerando relatório HTML...")
        self.show_progress(True)
        
        def export_task():
            try:
                success = self.smarttour.export_report(filename)
                
                if success:
                    message = f"Relatório salvo em: {filename}"
                    self.root.after(0, lambda: self.on_report_exported(True, message, filename))
                else:
                    message = "Erro ao gerar relatório HTML"
                    self.root.after(0, lambda: self.on_report_exported(False, message, None))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_report_exported(False, f"Erro: {str(e)}", None))
        
        threading.Thread(target=export_task, daemon=True).start()
    
    def on_report_exported(self, success, message, filename):
        """Callback quando relatório é exportado"""
        self.show_progress(False)
        
        if success:
            self.add_log(message)
            self.update_status("🟢 Relatório HTML gerado com sucesso")
            self.last_report_path = filename
            
            result = messagebox.askyesno("Sucesso", 
                                       message + "\n\nDeseja abrir o relatório agora?")
            if result:
                self.open_report(filename)
        else:
            self.add_log(f"ERRO: {message}")
            self.update_status("🔴 Erro na geração do relatório")
            messagebox.showerror("Erro", message)
    
    def open_report(self, filepath=None):
        """Abre relatório no navegador"""
        if not filepath:
            # Procurar arquivo padrão
            default_path = "smarttour_angola_report.html"
            if os.path.exists(default_path):
                filepath = default_path
            elif hasattr(self, 'last_report_path'):
                filepath = self.last_report_path
            else:
                messagebox.showwarning("Aviso", "Nenhum relatório encontrado. Gere um relatório primeiro!")
                return
        
        try:
            # Abrir no navegador
            webbrowser.open(f"file://{os.path.abspath(filepath)}")
            self.add_log(f"Relatório aberto: {Path(filepath).name}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o relatório: {str(e)}")
    
    def run(self):
        """Executa a aplicação"""
        self.add_log("Interface desktop carregada com sucesso")
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        app = SmartTourDesktop()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação:\n{str(e)}")

if __name__ == "__main__":
    main()
