import pandas as pd
from PyQt5 import QtWidgets, uic
from Model.arboVirose import *
from Model.tab import *
from Model.plot import *
from Model.geoPlot import *
from Model.QtExtras import *

class AppGui(QtWidgets.QMainWindow):
  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modelagem ArboBA")
  
        self.UiComponents()
        
        self.iniciar()
  
    def UiComponents(self):
        self.tela_inicial = uic.loadUi("./Gui/tela_inicial.ui")
        self.sair_confirmacao = uic.loadUi("./Gui/sair.ui")
        self.tela_selecao = uic.loadUi("./Gui/tela_selecao.ui")
        self.tela_periodo = uic.loadUi("./Gui/periodo.ui")
        self.tela_df = uic.loadUi("./Gui/tela_df.ui")
        self.tela_tab = uic.loadUi("./Gui/tela_tab.ui")
        
    def iniciar(self):
        self.tela_inicial.iniciarButton.clicked.connect(self.selecao)
        self.tela_inicial.sobreButton.clicked.connect(self.tela_inicial.frameInicial.close)
        self.tela_inicial.confirmarButton.clicked.connect(self.tela_inicial.frameInicial.show)
        self.tela_inicial.sairButton.clicked.connect(self.sair)
        
        self.tela_inicial.show()
        
    def sair(self):
        self.sair_confirmacao.show()
        self.sair_confirmacao.buttonBox.accepted.connect(QtWidgets.QApplication.quit)

    def selecao(self):
        self.tela_inicial.close()
        self.tela_selecao.confirmarArbo.clicked.connect(self.procurarArbo)
        self.tela_selecao.confirmarResto.clicked.connect(self.procurarDf)
        self.tela_selecao.show()
        
    def procurarArbo(self):
        self.tela_selecao.selecao.clear()
        content = self.tela_selecao.arboVirose.currentText()
        self.arbo = arboVirose(content)
        self.arbo.obterInfo()
        
        coluna_disp = ['Ano da Notificação', 'Mês da Notificação', 'Sexo', 'Fx Etária SINAN']
        if content == 'Dengue':
            coluna_disp.append('Ano do Óbito')
        
        self.tela_selecao.selecao.addItems(coluna_disp)
        
        self.tela_selecao.periodo.clicked.connect(self.setPeriodo)
    
    def setPeriodo(self):
        self.tela_periodo.listPeriodos.clear()
        self.tela_periodo.show()
        self.tela_periodo.listPeriodos.addItems(self.arbo.periodo)
        self.tela_periodo.buttonBox.accepted.connect(self.getPeriodos)
        
    def getPeriodos(self):
        self.periodo = [item.text() for item in self.tela_periodo.listPeriodos.selectedItems()]

    def procurarDf(self):
        if (self.tela_selecao.selecao.count() > 0 and len(self.periodo) > 0):
            self.tela_selecao.frame.close()
            self.df = self.arbo.obterDf('Município', self.tela_selecao.selecao.currentText(), self.periodo)
            model = pandasModel(self.df)
            self.tela_selecao.dataframe.setModel(model)
            self.tela_selecao.avancar.clicked.connect(self.getDf)
            
    def getDf(self):
        if (self.tela_selecao.selecao.currentText() == 'Ano da Notificação'):
            self.tela_selecao.close()
            model = pandasModel(self.df)
            self.tela_df.dataframe.setModel(model)
            self.tela_df.label.setText(f'{self.arbo.arbo_v}')
            self.tela_df.comboAno.addItems(list(self.df.columns[2:]))
            self.tela_df.comboAno_2.addItems(list(self.df.columns[2:]))
            self.tela_df.comboAno_3.addItems(list(self.df.columns[2:]))
            self.tela_df.pltButton.clicked.connect(self.dfPlt)
            self.tela_df.tabButton.clicked.connect(self.dfTab)
            self.tela_df.geoRefButton.clicked.connect(self.geoRef)
            self.tela_df.show()
        else:
            plot = plotGraficos(self.df, self.arbo.arbo_v, 'Município', self.tela_selecao.selecao.currentText(), list(self.df.columns[2:]))
            plot.definirPlotagem()
            
    def dfPlt(self):
        plot = plotGraficos(self.df, self.arbo.arbo_v, 'Município', self.tela_selecao.selecao.currentText(), list(self.df.columns[2:]))
        plot.definirPlotagem()
    
    def dfTab(self):
        if (self.tela_df.comboAno_2.currentText() != self.tela_df.comboAno_3.currentText()):
            self.tela_df.close()
            self.tela_tab.show()
            self.tela_tab.label.setText(f'{self.arbo.arbo_v} - Maiores Casos/Hab 100M {self.tela_df.comboAno_2.currentText()}')
            self.tab = tabArbo(self.arbo.arbo_v, self.df, [self.tela_df.comboAno_2.currentText(), self.tela_df.comboAno_3.currentText()])
            self.tela_tab.label_2.setText(f'{self.tab.Tx}')
            model = pandasModel(self.tab.table_1)
            self.tela_tab.dataframe.setModel(model)
            self.tela_tab.confirmarButton.clicked.connect(self.dfTab_1)
    
    def dfTab_1(self):
        self.tela_tab.label.setText(f'{self.arbo.arbo_v} - Maiores Casos/Hab 100M {self.tela_df.comboAno_3.currentText()}')
        model = pandasModel(self.tab.table_2)
        self.tela_tab.dataframe.setModel(model)
        self.tela_tab.confirmarButton.clicked.connect(self.dfTab_2)
    
    def dfTab_2(self):
        self.tela_tab.label.setText(f'{self.arbo.arbo_v} - Total de Casos por ano')
        model = pandasModel(self.tab.total_casos)
        self.tela_tab.dataframe.setModel(model)
        self.tela_tab.confirmarButton.clicked.connect(QtWidgets.QApplication.quit)
            
    def geoRef(self):
        df = geoRef(self.df)
        if (self.tela_df.comboPlot.currentText() == 'Automática - Casos por Município'):
            df.plotAuto(self.tela_df.comboAno.currentText())
        elif (self.tela_df.comboPlot.currentText() == 'Sturges - Casos por Município'):
            df.plotSturges(self.tela_df.comboAno.currentText())
        elif (self.tela_df.comboPlot.currentText() == 'Automática - Casos por 100 mil habitantes'):
            df.plotCasos100milAuto(self.tela_df.comboAno.currentText())
        elif (self.tela_df.comboPlot.currentText() == 'Sturges - Casos por 100 mil habitantes'):
            df.plotCasos100milSturges(self.tela_df.comboAno.currentText())