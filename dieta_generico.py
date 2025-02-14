# Daniel Triviño
# María Paula Murillo

# Importar librerías
import pyomo.environ as pyo
import pandas as pd
from pyomo.opt import SolverFactory
# Cargar datos
df = pd.read_csv("data.csv")
df_costs = df[['Calorias', 'Proteinas',
               'Azucar', 'Grasa', 'Carbohidratos']]
print(df)
print(df_costs)

df_constraints = pd.read_csv("constraints.csv")
df_constraints.fillna({'Limite superior': float('inf')}, inplace=True)
df_constraints.fillna({'Limite inferior': 0}, inplace=True)
print(df_constraints)

# Definición de conjuntos
n_nutrients = 5
size = df.shape

model = pyo.ConcreteModel(name="Distribución de alimentos")
model.A = pyo.Set(initialize=df['#'].to_list())
model.N = pyo.RangeSet(n_nutrients)

# Creación de modelo

# Definición de parámetros
param_precios = {k: v for k, v in zip(df['#'], df['Precio'])}
param_costos = {(a, n): df_costs.iloc[a-1, n-1]
                for a in model.A for n in model.N}


param_lower_bounds = {k: v for k, v in zip(
    df_constraints['#'], df_constraints['Limite inferior'])}
param_upper_bounds = {k: v for k, v in zip(
    df_constraints['#'], df_constraints['Limite superior'])}

model.P = pyo.Param(model.A, name="Precios", initialize=param_precios)
model.C = pyo.Param(
    model.A, model.N, name="Costos Nutricionales", initialize=param_costos)
model.L = pyo.Param(model.N, name="Limite inferior",
                    initialize=param_lower_bounds)
model.U = pyo.Param(model.N, name="Limite superior",
                    initialize=param_upper_bounds)

# Definición de variable objetivo
model.x = pyo.Var(model.A, domain=pyo.NonNegativeReals)

# Función objetivo


def obj(model):
    return sum(model.P[a] * model.x[a] for a in model.A)


model.objective = pyo.Objective(name="objective",
                                expr=obj, sense=pyo.minimize)

# Restricciones
model.nutrient_bounds = pyo.Constraint(
    model.N,
    rule=lambda model, n:
        pyo.inequality(model.L[n], sum(model.x[a]*model.C[a, n]
                       for a in model.A), model.U[n])
)

SolverFactory('glpk').solve(model)
model.display()
