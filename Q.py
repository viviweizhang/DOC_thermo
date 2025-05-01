#%%

import numpy as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd
import math
import os
from sympy import symbols, Eq, solve, nsolve, re,S, Abs
from matplotlib import colors
colors.XKCD_COLORS
from matplotlib import patheffects
from scipy.optimize import curve_fit
from matplotlib import cm, ticker
from matplotlib.collections import LineCollection
from matplotlib.colors import LogNorm
from matplotlib import font_manager
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch
from scipy.optimize import minimize



DIC = 2.5e-3       # mol/L
k_co2 = 10**(-6.4)
k_co3 = 10**(-10.3)

#original ocean concentration:
i = 8.1
H = 10 ** (-i)
OH = 10 ** (-14) / H
CO2_0 = DIC / (1 + k_co2 / H + k_co2*k_co3 / (H) ** 2)
HCO3_0 = DIC / (1 + H / k_co2 + k_co3 / H)
CO3_0 = DIC / (1 + H / k_co3 + (H) ** 2 / k_co2*k_co3)

F = 96485.3321 #s A / mol





# %%
from scipy.optimize import fsolve
df = pd.read_excel("base & acid_mol.xlsx")
pH_values = []
Q_base = []
Q_acid = []

for index, row in df.iterrows():
    pH_final = row.iloc[0]  # pH is the first column
    CO2 = row.iloc[1]  
    HCO3 = row.iloc[2]
    CO3 = row.iloc[3]
    CaMgCO32 = row.iloc[6]
    MgOH2 = row.iloc[7]  # MgOH2 is the 8th column
    CaCO3 = row.iloc[8]
    CaOH2 = row.iloc[9]
    Q = (2 * MgOH2 + 2 * CaOH2 + 2*CaMgCO32 + CaCO3 + CO3- CO3_0 - (CO2-CO2_0) - 10**(8.1-14) + 10**(pH_final-14))*F
    if Q < 0:
        Q = None
        Q1 = ((CO2-CO2_0) -CO3+ CO3_0 -2*CaMgCO32 + 10**(-pH_final) - 10**(-8.1))*F

    else:
        Q1 = None
    
    pH_values.append(pH_final)
    Q_base.append(Q)
    Q_acid.append(Q1)


df_output = pd.DataFrame({
    'pH': pH_values,
    'Q_base': Q_base,
    'Q_acid': Q_acid,
})

df_output.to_excel("output_Q.xlsx", index=False)










# %%
