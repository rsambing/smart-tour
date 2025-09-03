# ///////////////////////////////////////////////////////////////
#
# SmartTour Angola - App Functions
# Funções simplificadas da aplicação
#
# ///////////////////////////////////////////////////////////////

# SMARTTOUR INTEGRATION
# ///////////////////////////////////////////////////////////////
import sys
from pathlib import Path

# Add parent directory to path for smarttour import
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

try:
    from smarttour_app import smarttour_app
    SMARTTOUR_AVAILABLE = True
except ImportError as e:
    print(f"SmartTour não disponível: {e}")
    SMARTTOUR_AVAILABLE = False

# SIMPLIFIED APP FUNCTIONS
# ///////////////////////////////////////////////////////////////
class AppFunctions:
    """Funções simplificadas da aplicação SmartTour"""
    
    def __init__(self):
        self.smarttour_initialized = False
        
        if SMARTTOUR_AVAILABLE:
            self.init_smarttour()
    
    def init_smarttour(self):
        """Inicializa o SmartTour"""
        try:
            # Carrega dados de exemplo
            smarttour_app.load_sample_data()
            
            # Executa análise
            if smarttour_app.data_loaded:
                success = smarttour_app.perform_analysis()
                if success:
                    self.smarttour_initialized = True
                    print("SmartTour inicializado com sucesso!")
                    return True
            
            print("Falha ao inicializar SmartTour")
            return False
                
        except Exception as e:
            print(f"Erro ao inicializar SmartTour: {e}")
            return False
    
    def get_smarttour_status(self):
        """Retorna status do SmartTour"""
        if not SMARTTOUR_AVAILABLE or not self.smarttour_initialized:
            return {}
        
        try:
            return smarttour_app.get_status()
        except Exception as e:
            print(f"Erro ao obter status: {e}")
            return {}
    
    def export_report(self, filename="smarttour_report.html"):
        """Exporta relatório do SmartTour"""
        if not SMARTTOUR_AVAILABLE or not self.smarttour_initialized:
            return False
        
        try:
            return smarttour_app.export_analysis_report(filename)
        except Exception as e:
            print(f"Erro ao exportar relatório: {e}")
            return False
    
    def get_province_analysis(self, province_name: str):
        """Obtém análise detalhada de uma província"""
        if not SMARTTOUR_AVAILABLE or not self.smarttour_initialized:
            return {}
        
        try:
            return smarttour_app.get_province_analysis(province_name)
        except Exception as e:
            print(f"Erro ao obter análise da província {province_name}: {e}")
            return {}
    
    def get_kpis(self):
        """Obtém KPIs principais"""
        if not SMARTTOUR_AVAILABLE or not self.smarttour_initialized:
            return {}
        
        try:
            return smarttour_app.kpis
        except Exception as e:
            print(f"Erro ao obter KPIs: {e}")
            return {}

# MAIN FILE
# ///////////////////////////////////////////////////////////////
from main import *
from modules.app_settings import Settings

# WITH ACCESS TO MAIN WINDOW WIDGETS
# ///////////////////////////////////////////////////////////////
class AppFunctions(MainWindow):
    def setThemeHack(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: #495474;"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: #495474;"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
        background-color: #566388;
        """

        # SET MANUAL STYLES
        self.ui.lineEdit.setStyleSheet("background-color: #6272a4;")
        self.ui.pushButton.setStyleSheet("background-color: #6272a4;")
        self.ui.plainTextEdit.setStyleSheet("background-color: #6272a4;")
        self.ui.tableWidget.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.scrollArea.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.comboBox.setStyleSheet("background-color: #6272a4;")
        self.ui.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.commandLinkButton.setStyleSheet("color: #ff79c6;")
