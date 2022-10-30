import pandas as pd
import numpy as np

class tabArbo():
    def __init__(self, Arbo_V:str, df: pd, Anos: list):
        self.Arbo_V = Arbo_V
        self.df = df
        self.Anos = Anos
        self.setTable(df, Anos)
        
    def setTable(self, df, Ano):
        df.iloc[:, 2:] = df.iloc[:, 2:].astype('int32')
        censo = pd.read_pickle("./Datasets/ibge_2010.pkl")
        df = df.merge(censo, left_on='Município', right_on='Município')
        df[f'Casos/Hab 100M {Ano[0]}'] = (df[f'{Ano[0]}']/df["População 2010"]*100000)
        df[f'Casos/Hab 100M {Ano[0]}'] = df[f'Casos/Hab 100M {Ano[0]}'].astype('float32').round(2)
        df[f'Casos/Hab 100M {Ano[1]}'] = (df[f'{Ano[1]}']/df["População 2010"]*100000)
        df[f'Casos/Hab 100M {Ano[1]}'] = df[f'Casos/Hab 100M {Ano[1]}'].astype('float32').round(2)
        
        df[f'Tx Crescimento dos anos {Ano[0]} e {Ano[1]}'] = np.around((df[Ano[0]].astype('float32') - df[Ano[1]].astype('float32')).divide(df[Ano[1]].astype('float32')) * 100)
        table_1 = df.nlargest(10, f'Casos/Hab 100M {Ano[0]}')[['Código', 'Município', 'População 2010', f'{Ano[0]}', f'Casos/Hab 100M {Ano[0]}', f'Tx Crescimento dos anos {Ano[0]} e {Ano[1]}']]
        table_2 = df.nlargest(10, f'Casos/Hab 100M {Ano[1]}')[['Código', 'Município', 'População 2010', f'{Ano[1]}', f'Casos/Hab 100M {Ano[1]}', f'Tx Crescimento dos anos {Ano[0]} e {Ano[1]}']]
        total_casos = pd.DataFrame(df.iloc[:, 2:-3].sum(), df.columns[2:-3], columns=['Casos'])
        total_casos.Casos = total_casos.Casos.astype('int32')
        total_casos["População 2010"] = df["População 2010"].sum()
        total_casos["Casos/Hab 100M"] = round(total_casos.iloc[:, 0]/total_casos.loc[:, "População 2010"] * 100000, 1)
        
        taxa = round((total_casos.loc[f'{Ano[0]}'][0] - total_casos.loc[f'{Ano[1]}'][0]) / total_casos.loc[f'{Ano[1]}'][0] * 100, 1)
        self.Tx = str(f'Taxa de crescimento de {self.Arbo_V} do ano {Ano[1]} comparado {Ano[0]} foi de {taxa}%')
        
        self.table_1 = table_1
        self.table_2 = table_2
        self.total_casos = total_casos.reset_index().rename(columns={'index': 'Anos'})