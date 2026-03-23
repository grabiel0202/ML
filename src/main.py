import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 1. LER ARQUIVOS (SÓ 2000)
# ==============================

arquivos = glob.glob("C:/Users/sampaio.gss/Documents/ML/dados/2000/**/*.csv", recursive=True)

print(f"Arquivos encontrados: {len(arquivos)}")

dfs = []

for arq in arquivos:
    print(f"Lendo: {arq}")
    
    df_temp = pd.read_csv(
        arq,
        sep=';',
        encoding='latin1',
        skiprows=8,
        usecols=[
            "DATA (YYYY-MM-DD)",
            "HORA (UTC)",
            "PRECIPITAÇÃO TOTAL, HORÁRIO (mm)",
            "TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"
        ]
    )
    
    dfs.append(df_temp)

df = pd.concat(dfs)

# ==============================
# 2. LIMPEZA
# ==============================

df = df.replace("-9999", np.nan)
df = df.replace(-9999, np.nan)

# converter números
df["PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"] = pd.to_numeric(
    df["PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"], errors='coerce'
)

df["TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"] = pd.to_numeric(
    df["TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"], errors='coerce'
)

# ==============================
# 3. DATA
# ==============================

df["DATETIME"] = pd.to_datetime(
    df["DATA (YYYY-MM-DD)"] + " " + df["HORA (UTC)"],
    errors='coerce'
)

df = df.dropna(subset=["DATETIME"])
df = df.sort_values("DATETIME")

# ==============================
# 4. ANÁLISE SIMPLES
# ==============================

df["MES"] = df["DATETIME"].dt.month

temp_mes = df.groupby("MES")["TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"].mean()
chuva_mes = df.groupby("MES")["PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"].sum()

print(temp_mes)
print(chuva_mes)

# ==============================
# 5. GRÁFICOS
# ==============================

plt.figure()
temp_mes.plot()
plt.title("Temperatura média por mês - 2000")
plt.show()

plt.figure()
chuva_mes.plot()
plt.title("Chuva total por mês - 2000")
plt.show()