import math
import matplotlib
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np



class geoRef(object):
    def __init__(self, df):
        self.map = gpd.read_file("./Map/Map.shp")
        self.df = df
        self.atribuirCasos()
    
    def atribuirCasos(self):
        df_censo = pd.read_csv("./BA - IBGE 2010.csv")
        map = self.map.drop(columns="CODIGO")

        map = pd.merge(self.df, map, on=["Município"])
        map = pd.merge(df_censo.iloc[:, 1:], map, on=["Município"])

        map.iloc[:, 3:-1] = map.iloc[:, 3:-1].astype('int64')
        
        self.map = gpd.GeoDataFrame(map)
        
    def plotAuto(self, ano):
        self.map.plot(column = ano, cmap='coolwarm', linewidth=1, legend=True)
        
    def plotSturges(self, ano):
        map = self.map
        nc = math.ceil( 1 + 3.322 * math.log(len(map), 10) )
        intervalo = []
        for i in range (nc):
            intervalo.append(map[ano].quantile(nc * i/100))
        intervalo = sorted(set(intervalo))
        
        map.plot(column=ano, scheme='user_defined', classification_kwds={'bins':intervalo}, cmap='coolwarm', linewidth=1, legend=True)
        
    def plotCasos100milAuto(self, ano):
        map = self.map
        map["Casos_100.000hab"] = round(map.loc[:, ano]/map.loc[:, "População 2010"] * 100000, 0)
        
        map.plot(column="Casos_100.000hab", cmap='coolwarm', linewidth=1, legend=True)
        
    def plotCasos100milSturges(self, ano):
        map = self.map
        map["Casos_100.000hab"] = round(map.loc[:, ano]/map.loc[:, "População 2010"] * 100000, 0)
        nc = math.ceil( 1 + 3.322 * math.log(len(map), 10) )
        intervalo = []
        for i in range (nc):
            intervalo.append(map["Casos_100.000hab"].quantile(nc * i/100))
        intervalo = sorted(set(intervalo))
        
        map.plot(column="Casos_100.000hab", scheme='user_defined', classification_kwds={'bins':intervalo}, cmap='coolwarm', linewidth=1, legend=True)
        