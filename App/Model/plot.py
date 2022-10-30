import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class plotGraficos():
    def __init__(self, df, arbo_v, linha, coluna, periodo):
        plt.rcParams["figure.figsize"] = (10, 10)
        self.df, self.arbo_v, self.linha, self.coluna, self.periodo = df, arbo_v, linha, coluna, periodo

    def definirPlotagem(self):
        if self.coluna == 'Ano da Notificação':
            self.pltCasos()
        elif self.coluna == 'Ano do Óbito':
            self.pltObitos()
        elif self.coluna == 'Mês da Notificação':
            self.pltMes()
        elif self.coluna == 'Sexo':
            self.pltSexo()
        elif self.coluna == 'Fx Etária SINAN':
            self.pltFxEtaria()
        plt.show()

    def pltCasos(self):
        casos = self.df.iloc[:, 2:].astype('int64').sum()
        casos = pd.DataFrame(casos.values.tolist(), index = casos.index.to_list(), columns=["Casos"])
        plt.bar(casos.index, casos.iloc[:, 0], color="#103b6e")
        plt.xlabel("Anos")
        plt.ylabel("Casos")
        if self.arbo_v == "Dengue":
            plt.title("Dengue")
        elif self.arbo_v == "Chikungunya":
            plt.title("Chikungunya")
        elif self.arbo_v == "Zika":
            plt.title("Zika Vírus")
        plt.show()
          
    def pltObitos(self):
        obitos = self.df.iloc[:, 2:].astype('int64').sum()
        obitos = pd.DataFrame(obitos.values.tolist(), index = obitos.index.to_list(), columns=["Óbitos"])
        plt.bar(obitos.index, obitos.iloc[:, 0], color="#103b6e")
        plt.xlabel("Anos")
        plt.ylabel("Óbitos")
        plt.title("Dengue")
        plt.show()
        
    def pltMes(self):
        meses = self.df.iloc[:, 2:].astype('int64').sum()
        meses = pd.DataFrame(meses.values.tolist(), index = meses.index.to_list(), columns=["Meses"])
        plt.bar(meses.index, meses.iloc[:, 0], color="#103b6e")
        plt.xlabel("Meses")
        plt.ylabel("Casos")
        if self.arbo_v == "Dengue":
            plt.title(f"Dengue")
        elif self.arbo_v == "Chikungunya":
            plt.title(f"Chikungunya")
        elif self.arbo_v == "Zika":
            plt.title("Zika Vírus")
        plt.show()
            
    def pltSexo(self):
        sexo = self.df.iloc[:, 2:].astype('int64')
        sexo["Branco e Ignorado"] = sexo["Em Branco"] + sexo["Ignorado"]
        sexo = sexo.drop(columns=['Em Branco'])
        sexo = sexo.drop(columns=['Ignorado'])
        sexo = sexo.sum()
        sexo = pd.DataFrame(sexo.values.tolist(), index = sexo.index.to_list(), columns=["Sexo"])
        plt.bar(sexo.index, sexo.iloc[:, 0], color="#103b6e")
        plt.xlabel("Sexos")
        plt.ylabel("Casos")
        if self.arbo_v == "Dengue":
            plt.title(f"Dengue")
        elif self.arbo_v == "Chikungunya":
            plt.title(f"Chikungunya")
        elif self.arbo_v == "Zika":
            plt.title("Zika Vírus")
        plt.show()
            
    def pltFxEtaria(self):
        fx_etaria = self.df.iloc[:, 2:].astype('int64').sum()
        fx_etaria = pd.DataFrame(fx_etaria.values.tolist(), index = fx_etaria.index.to_list(), columns=["Faixa Etária"])

        Faixa = ["Menor que 1", "Entre 1 e 9", "Entre 10 e 19", "Entre 20 e 34", "Entre 35 e 49", "Entre 50 e 64", "Entre 65 e 79", "Maior que 80"]
        Casos = [fx_etaria.loc["<1 Ano"][0], fx_etaria.loc["1-4"][0] + fx_etaria.loc["5-9"][0], fx_etaria.loc["10-14"][0] + fx_etaria.loc["15-19"][0], fx_etaria.loc["20-34"][0], fx_etaria.loc["35-49"][0], fx_etaria.loc["50-64"][0], fx_etaria.loc["65-79"][0], fx_etaria.loc["80 e+"][0]]

        plt.bar(Faixa, Casos, color="#103b6e")
        plt.xlabel("Faixas")
        plt.ylabel("Casos")
        if self.arbo_v == "Dengue":
            plt.title(f"Dengue")
        elif self.arbo_v == "Chikungunya":
            plt.title(f"Chikungunya")
        elif self.arbo_v == "Zika":
            plt.title("Zika Vírus")
        plt.show()