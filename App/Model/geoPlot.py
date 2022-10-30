import math
import matplotlib
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

class geoRef(object):
    def __init__(self, df):
        plt.rcParams["figure.figsize"] = (10, 10)
        self.bahia = gpd.read_file("./Datasets/Map/Map.shp")
        self.df = df
        self.atribuirCasos()
    
    def atribuirCasos(self):
        censo = pd.read_pickle("./Datasets/ibge_2010.pkl")
        df = self.df.merge(censo, left_on='Município', right_on='Município')
        df = df.merge(self.bahia, left_on='Município', right_on='Município')
        df.drop(columns='CODIGO', inplace=True)
        df = gpd.GeoDataFrame(df)
        df[df.columns[2:-2]] = df[df.columns[2:-2]].astype('int32')
        self.bahia = df
        
    def plotAuto(self, ano):
        self.bahia.plot(column = ano, cmap='coolwarm', linewidth=1, legend=True)
        plt.show()
        
    def plotSturges(self, ano):
        bahia = self.bahia
        nc = math.ceil( 1 + 3.322 * math.log(len(bahia), 10) )
        intervalo = []
        for i in range (nc):
            intervalo.append(bahia[ano].quantile(nc * i/100))
        intervalo = sorted(set(intervalo))
        
        bahia.plot(column=ano, scheme='user_defined', classification_kwds={'bins':intervalo}, cmap='coolwarm', linewidth=1, legend=True)
        plt.show()
        
    def plotCasos100milAuto(self, ano):
        bahia = self.bahia
        bahia["Casos_100.000hab"] = round(bahia.loc[:, ano]/bahia.loc[:, "População 2010"] * 100000, 0)
        
        bahia.plot(column="Casos_100.000hab", cmap='coolwarm', linewidth=1, legend=True)
        plt.show()
        
    def plotCasos100milSturges(self, ano):
        bahia = self.bahia
        bahia["Casos_100.000hab"] = round(bahia.loc[:, ano]/bahia.loc[:, "População 2010"] * 100000, 0)
        nc = math.ceil( 1 + 3.322 * math.log(len(bahia), 10) )
        intervalo = []
        for i in range (nc):
            intervalo.append(bahia["Casos_100.000hab"].quantile(nc * i/100))
        intervalo = sorted(set(intervalo))
        
        bahia.plot(column="Casos_100.000hab", scheme='user_defined', classification_kwds={'bins':intervalo}, cmap='coolwarm', linewidth=1, legend=True)
        plt.show()