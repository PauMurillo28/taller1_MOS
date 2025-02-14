# Daniel Triviño
# María Paula Murillo

# Importar librerías
import pyomo.environ as pyo
import pandas as pd
from pyomo.opt import SolverFactory
# Cargar datos
df = pd.read_csv("data.csv")
df_costs = df[['Calorías (Cal)', 'Proteínas (gr)',
               'Azúcar (gr)', 'Grasa (gr)', 'Carbohidratos (gr)']]
print(df)
print(df_costs)

# Definición de conjuntos
n_nutrients = 5
size = df.shape

model = pyo.ConcreteModel(name="Distribución de alimentos")
model.A = pyo.Set(initialize=df['No'].to_list())
model.N = pyo.RangeSet(n_nutrients)

# Creación de modelo

# Definición de parámetros
param_precios = {k: v for k, v in zip(df['No'], df['Precio (COP)'])}
param_costos = {(a, n): df_costs.iloc[a-1,n-1] for a in model.A for n in model.N}
param_lower_bounds = {k:v for k, v in zip()}
print(param_costos)


model.P = pyo.Param(model.A, name="Precios")
model.C = pyo.Param(model.A, model.N, name="Costos Nutricionales")
model.L = pyo.Param(model.N, name="Limite inferior")
model.U = pyo.Param(model.N, name="Limite superior")

# Definición de variable objetivo
model.x = pyo.Var(model.A, domain=pyo.NonNegativeReals)
