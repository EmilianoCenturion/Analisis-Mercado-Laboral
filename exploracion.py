import pandas as pd
import os

ruta = "datos_eph_P21actualizado_aglomeradofiltrado"

dfs = []

for archivo in os.listdir(ruta):
    if archivo.endswith(".txt"):
        direc = os.path.join(ruta, archivo)
        df = pd.read_csv(direc, sep= ";", decimal= ",", encoding= "latin1", low_memory=False)
        dfs.append(df)

df_total = pd.concat(dfs, ignore_index= True)

# Filtramos los dos aglomerados elegidos: GBA (33) y GRAN CORDOBA (13) 
df_total = df_total[df_total["AGLOMERADO"].isin([33 , 13])]

# ────────────────────────────────────────────────────────────
#                            Punto 1 
# ────────────────────────────────────────────────────────────

print("======================== EXPLORACIÓN GENERAL ========================")
print("Cantidad de casos:", len(df_total))
print("\nCasos por aglomerado:")
print(df_total["AGLOMERADO"].value_counts())

print("\nEdad (CH06):") # se evalua la si es mayor o igual a 0 porque -1 no es una edad real 
print(df_total[df_total["CH06"] >= 0]["CH06"].describe())

print("\nSexo (CH04):") # 1 varon, 2 mujer
print(df_total["CH04"].value_counts(dropna=False))

print("\nCondicion de actividad (ESTADO):") # 1 = ocupado, 2 = desocupado
print(df_total["ESTADO"].value_counts(dropna=False).sort_index())

print("\nNivel Educativo (NIVEL_ED):")
print(df_total["NIVEL_ED"].value_counts(dropna=False).sort_index())


print("\n======================== VARIABLES DE EMPLEO ========================")
""" 
Variables del empleo: solo tienen sentido para los ocupados
Un desocupado o inactivo no tiene rama ni calificaion de empleo, asi que las miro solo sobre los ocupados (ESTADO == 1) para no contar vacios

"""
ocupados = df_total[df_total["ESTADO"] == 1]

#a qué se dedica la empresa donde trabaja
print("\nRama de actividad (PP04B_COD) - solo ocupados:") 
print("Valores distintos:", ocupados["PP04B_COD"].nunique())
print(ocupados["PP04B_COD"].value_counts(dropna=False).head(10))


print("\nCalificacion de la ocupacion (PP04D_COD) - solo ocupados:")
print("Valores distintos:", ocupados["PP04D_COD"].nunique())
print(ocupados["PP04D_COD"].value_counts(dropna=False).head(10))

# El ultimo digito de PP04D_COD indica el nivel de calificacion de la tarea.
    # Profesional - Requiere título universitario
    # Técnica - Requiere formación técnica o terciaria
    # Operativa - Requiere capacitación práctica
    # No calificada - No requiere formación específica
ocupados = ocupados.copy()
calif_num = pd.to_numeric(ocupados["PP04D_COD"], errors="coerce")
ocupados["calif"] = calif_num.dropna().astype("int64").astype(str).str[-1]
calif_nombre = {"1": "Profesional", "2": "Tecnica", "3": "Operativa", "4": "No calificada"}
ocupados["calif_nombre"] = ocupados["calif"].map(calif_nombre).fillna("Sin dato")

print("\nNivel de calificacion (ultimo digito de PP04D_COD) - solo ocupados:")
print(ocupados["calif_nombre"].value_counts(dropna=False))


print("\n======================== NO RESPUESTA EN P21 ========================")
# 2) No respuesta en ingresos (P21 == -9), mirando solo a los ocupados
print("\n--- No respuesta a ingresos (P21) ---")
for aglo in [33, 13]:
    sub = ocupados[ocupados["AGLOMERADO"] == aglo]
    no_resp = (sub["P21"] == -9).sum()
    total = len(sub)
    print(f"Aglomerado {aglo}: {no_resp} de {total} no respondieron ({100*no_resp/total:.1f}%)")


print("\n======================== DETECCION DUPLICADOS ========================")

print("Personas repetidas:", df_total.duplicated(subset=["ANO4","TRIMESTRE","CODUSU","NRO_HOGAR","COMPONENTE"]).sum())


print("\n======================== VALORES ATIPICOS ========================")

ocupados["P21"] = pd.to_numeric(ocupados["P21"], errors="coerce")
p21_validos = ocupados[(ocupados["P21"] > 0) & (ocupados["P21"].notna())]["P21"]

Q1 = p21_validos.quantile(0.25)
Q3 = p21_validos.quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = ocupados[
    (ocupados["P21"] > 0) &
    (ocupados["P21"].notna()) &
    ((ocupados["P21"] < limite_inferior) | (ocupados["P21"] > limite_superior))
]

print(f"Q1: {Q1:.2f}  |  Q3: {Q3:.2f}  |  IQR: {IQR:.2f}")
print(f"Límite inferior: {limite_inferior:.2f}  |  Límite superior: {limite_superior:.2f}")
print(f"Outliers detectados: {len(outliers)} ({100*len(outliers)/len(p21_validos):.1f}%)")
print("\nOutliers por aglomerado:")
print(outliers["AGLOMERADO"].value_counts())

