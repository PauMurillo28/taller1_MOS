#Daniel Triviño
#María Paula Murillo

# Importar librerías
from  pyomo.environ  import *
import pandas as pd
from pyomo.opt import SolverFactory
model = ConcreteModel ()

#Cargar datos
df_alimentos = pd.read_csv("tabla_alimentos.csv")
print("Data Alimentos")
print(df_alimentos)

#Dicicionario donde cada alimento tiene asociado sus beneficios
dic_calorias = {k: v for k, v in zip(df_alimentos['# Alimento'], df_alimentos['Calorias'])}
dic_proteinas = {k: v for k, v in zip(df_alimentos['# Alimento'], df_alimentos['Proteinas'])}
dic_azucar = {k: v for k, v in zip(df_alimentos['# Alimento'], df_alimentos['Azucar'])}
dic_grasa = {k: v for k, v in zip(df_alimentos['# Alimento'], df_alimentos['Grasa'])}
dic_carbohidratos = {k: v for k, v in zip(df_alimentos['# Alimento'], df_alimentos['Carbohidratos'])}
dic_precio = {k: v for k, v in zip(df_alimentos['# Alimento'], df_alimentos['Precio'])}

#Conjuntos
#Conjunto de Beneficios
#1->Calorías
#2->Proteínas
#3->Azucar
#4->Grasa
#5->Carbohidratos
model.B = RangeSet(1, 5)
#Conjunto de Alimentos
#1->Carne
#2->Arroz
#3->Leche
#4->Pan
model.A = RangeSet(1, 4)

#Parametros
#Calorias
model.C = Param(model.A,  name="Calorias", initialize=dic_calorias)
#Proteinas
model.P = Param(model.A, name="Proteinas", initialize=dic_proteinas)
#Azucar
model.AZ = Param(model.A, name="Azucar", initialize=dic_azucar)
#Grasa
model.G = Param(model.A, name="Grasa", initialize=dic_grasa)
#Carbohidratos
model.CA = Param(model.A, name="Carbohidratos", initialize=dic_carbohidratos)
#Precio
model.PR = Param(model.A, name="Precio", initialize=dic_precio)

#Variable de decisión
model.x = Var(model.A, domain=Binary)

#Función objetivo
model.obj = Objective(expr=3000*model.B[0][a] + 1000*model.B[1][a] + 600*model.B[2][a] + 700*model.B, sense=minimize)
