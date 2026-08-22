import pandas as pd
import os

ruta = "datos_eph_P21actualizado_aglomeradofiltrado"

dfs = []

for archivo in os.listdir(ruta):
    if archivo.endswith(".txt"):
        direc = os.path.join(ruta, archivo)
        df = pd.read_csv(direc, sep= ";", decimal= ",", encoding= "latin1", low_memory=False)
        dfs.append(df)

df_total = pd.concat(dfs, ignore_index= True).copy()

# Filtramos los dos aglomerados elegidos: GBA (33) y GRAN CORDOBA (13) 
df_total = df_total[df_total["AGLOMERADO"].isin([33 , 13])]

# ────────────────────────────────────────────────────────────
#                            Punto 2 
# ────────────────────────────────────────────────────────────

print("========== TASAS POR PERÍODO Y AGLOMERADO ==========")
df_total["PERIODO"] = df_total["ANO4"].astype(str) + "_T" + df_total["TRIMESTRE"].astype(str)

# Convertir P21Actualizado a número
df_total["P21Actualizado"] = pd.to_numeric(df_total["P21Actualizado"], errors="coerce")

def calcular_tasas(grupo):
    # Solo mayores de 14 años (excluimos ESTADO == 4 que son menores de 10)
    poblacion = grupo[grupo["ESTADO"].isin([1, 2, 3])]
    
    ocupados    = poblacion[poblacion["ESTADO"] == 1]["PONDERA"].sum()
    desocupados = poblacion[poblacion["ESTADO"] == 2]["PONDERA"].sum()
    total       = poblacion["PONDERA"].sum()
    activos     = ocupados + desocupados

    tasa_actividad    = activos / total * 100       if total   > 0 else None
    tasa_empleo       = ocupados / total * 100      if total   > 0 else None
    tasa_desocupacion = desocupados / activos * 100 if activos > 0 else None

    return pd.Series({
        "Tasa actividad":     round(tasa_actividad, 2),
        "Tasa empleo":        round(tasa_empleo, 2),
        "Tasa desocupacion":  round(tasa_desocupacion, 2)
    })

tasas = df_total.groupby(["PERIODO", "AGLOMERADO"]).apply(calcular_tasas).reset_index()
tasas = tasas.sort_values(["AGLOMERADO", "PERIODO"])

print(tasas.to_string(index=False))





print("\n========== INGRESOS REALES POR PERÍODO Y AGLOMERADO ==========")

def mediana_ponderada(valores, pesos, cuantil=0.5):
    df_temp = pd.DataFrame({"v": valores, "p": pesos}).dropna()
    df_temp = df_temp[df_temp["p"] > 0]  # excluye pesos cero
    df_temp = df_temp.sort_values("v")
    
    df_temp["p_acum"] = df_temp["p"].cumsum()
    total_peso = df_temp["p"].sum()
    
    corte = total_peso * cuantil
    return df_temp[df_temp["p_acum"] >= corte]["v"].iloc[0]

ocupados = df_total[
    (df_total["ESTADO"] == 1) &
    (df_total["P21Actualizado"] > 0) &
    (df_total["P21Actualizado"].notna())
].copy()

ing = ocupados.groupby(["PERIODO", "AGLOMERADO"]).apply(
    lambda g: pd.Series({
        "Media":   (g["P21Actualizado"] * g["PONDIIO"]).sum() / g["PONDIIO"].sum(),
        "Mediana": mediana_ponderada(g["P21Actualizado"], g["PONDIIO"]),
        "Q1":      mediana_ponderada(g["P21Actualizado"], g["PONDIIO"], cuantil=0.25),
        "Q3":      mediana_ponderada(g["P21Actualizado"], g["PONDIIO"], cuantil=0.75)
    })
).reset_index()

ingresos = ing.sort_values(["AGLOMERADO", "PERIODO"])
ingresos[["Media", "Mediana", "Q1", "Q3"]] = ingresos[["Media", "Mediana", "Q1", "Q3"]].round(2)

print(ingresos.to_string(index=False))






print("\n========== INGRESOS POR NIVEL EDUCATIVO ==========")
nivel_ed_nombres = {
    1: "Primario incompleto",
    2: "Primario completo",
    3: "Secundario incompleto",
    4: "Secundario completo",
    5: "Superior incompleto",
    6: "Superior completo",
    7: "Sin instrucción"
}

ocupados["Nivel educativo"] = ocupados["NIVEL_ED"].map(nivel_ed_nombres).fillna("Sin dato")

ing_educativo = ocupados.groupby(["PERIODO", "AGLOMERADO", "Nivel educativo"]).apply(
    lambda g: pd.Series({
        "Mediana": mediana_ponderada(g["P21Actualizado"], g["PONDIIO"])
    })
).reset_index()

ing_educativo = ing_educativo.sort_values(["AGLOMERADO", "PERIODO", "Nivel educativo"])
print(ing_educativo.to_string(index=False))





print("\n========== INGRESOS POR SEXO ==========")
ocupados["Sexo"] = ocupados["CH04"].map({1: "Varón", 2: "Mujer"})

ing_sexo = ocupados.groupby(["PERIODO", "AGLOMERADO", "Sexo"]).apply(
    lambda g: pd.Series({
        "Mediana": mediana_ponderada(g["P21Actualizado"], g["PONDIIO"])
    })
).reset_index()

ing_sexo = ing_sexo.sort_values(["AGLOMERADO", "PERIODO"])
print(ing_sexo.to_string(index=False))





print("\n========== INGRESOS POR RANGO DE EDAD ==========")
bins  = [14, 25, 35, 45, 55, 65, 200]
labels = ["14-25", "26-35", "36-45", "46-55", "56-65", "66+"]

ocupados["CH06"] = pd.to_numeric(ocupados["CH06"], errors="coerce")

ocupados["Rango de edad"] = pd.cut(
    ocupados["CH06"],
    bins=bins,
    labels=labels,
    right=True
)

ing_edad = ocupados.groupby(["PERIODO", "AGLOMERADO", "Rango de edad"]).apply(
    lambda g: pd.Series({
        "Mediana": mediana_ponderada(g["P21Actualizado"], g["PONDIIO"])
    })
).reset_index()

ing_edad = ing_edad.sort_values(["AGLOMERADO", "PERIODO", "Rango de edad"])
print(ing_edad.to_string(index=False))





print("\n========== INGRESOS POR NIVEL DE CALIFICACIÓN ==========")
calif_num = pd.to_numeric(ocupados["PP04D_COD"], errors="coerce")
ocupados["calif"] = calif_num.dropna().astype("int64").astype(str).str[-1]
calif_nombres = {"1": "Profesional", "2": "Técnica", "3": "Operativa", "4": "No calificada"}
ocupados["Nombre de calificacion"] = ocupados["calif"].map(calif_nombres).fillna("Sin dato")

ing_calif = ocupados.groupby(["PERIODO", "AGLOMERADO", "Nombre de calificacion"]).apply(
    lambda g: pd.Series({
        "Mediana": mediana_ponderada(g["P21Actualizado"], g["PONDIIO"])
    })
).reset_index()

ing_calif = ing_calif.sort_values(["AGLOMERADO", "PERIODO"])
print(ing_calif.to_string(index=False))





print("\n========== INGRESOS POR RAMA DE ACTIVIDAD ==========----------------------- REVISAR")
ocupados["PP04B_COD"] = pd.to_numeric(ocupados["PP04B_COD"], errors="coerce")
ocupados["rama"] = ocupados["PP04B_COD"].dropna().astype("int64").astype(str).str[0]

rama_nombres = {
    "0": "Agricultura",
    "1": "Industria",
    "2": "Construcción",
    "3": "Comercio",
    "4": "Transporte",
    "5": "Servicios financieros",
    "6": "Servicios sociales",
    "7": "Administración pública",
    "8": "Servicio doméstico",
    "9": "Otros"
}

ocupados["Rama"] = ocupados["rama"].map(rama_nombres).fillna("Sin dato")

ing_rama = ocupados.groupby(["PERIODO", "AGLOMERADO", "Rama"]).apply(
    lambda g: pd.Series({
        "Mediana": mediana_ponderada(g["P21Actualizado"], g["PONDIIO"])
    })
).reset_index()

ing_rama = ing_rama.sort_values(["AGLOMERADO", "PERIODO", "Rama"])
print(ing_rama.to_string(index=False))



# ── GUARDAR RESULTADOS PARA GRÁFICOS ────────────────────────
os.makedirs("resultados", exist_ok=True)

tasas.to_csv("resultados/tasas.csv", index=False)
ingresos.to_csv("resultados/ingresos.csv", index=False)
ing_educativo.to_csv("resultados/ing_educativo.csv", index=False)
ing_sexo.to_csv("resultados/ing_sexo.csv", index=False)
ing_edad.to_csv("resultados/ing_edad.csv", index=False)
ing_calif.to_csv("resultados/ing_calif.csv", index=False)
ing_rama.to_csv("resultados/ing_rama.csv", index=False)

print("\nResultados guardados en carpeta /resultados")
