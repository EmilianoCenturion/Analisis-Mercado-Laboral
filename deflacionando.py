import pandas as pd

periodo_archivo = "2024_T4"

ruta = f"datos_eph/{periodo_archivo}.txt"

rutaGuardado = f"datos_eph_P21actualizado_aglomeradofiltrado/{periodo_archivo}_actualizado.txt"


inflacion = {

    "2017_T1": 0.061,
    "2017_T2": 0.053,
    "2017_T3": 0.050,
    "2017_T4": 0.060,

    "2018_T1": 0.065,
    "2018_T2": 0.085,
    "2018_T3": 0.135,
    "2018_T4": 0.112,

    "2019_T1": 0.114,
    "2019_T2": 0.092,
    "2019_T3": 0.121,
    "2019_T4": 0.113,

    "2020_T1": 0.076,
    "2020_T2": 0.052,
    "2020_T3": 0.074,
    "2020_T4": 0.110,

    "2021_T1": 0.124,
    "2021_T2": 0.106,
    "2021_T3": 0.090,
    "2021_T4": 0.098,

    "2022_T1": 0.153,
    "2022_T2": 0.164,
    "2022_T3": 0.206,
    "2022_T4": 0.163,

    "2023_T1": 0.203,
    "2023_T2": 0.222,
    "2023_T3": 0.314,
    "2023_T4": 0.466,

    "2024_T1": 0.448,
    "2024_T2": 0.176,
    "2024_T3": 0.117,
    "2024_T4": 0.078,

    "2025_T1": 0.083,
    "2025_T2": 0.059,
    "2025_T3": 0.059,
    "2025_T4": 0.076
}


periodos = list(inflacion.keys())


def calcular_factor(periodo_actual):

    inicio = periodos.index(periodo_actual)
    fin = periodos.index("2025_T4")

    factor = 1

    for periodo in periodos[inicio+1:fin+1]:
        factor *= (1 + inflacion[periodo])

    return factor



def actualizar_p21(valor, periodo_archivo):

    # Mantener vacíos y -9 (Aquí ira la logica para filtrarlo de estos casos)
    if pd.isna(valor) or valor == -9:
        return valor

    factor = calcular_factor(periodo_archivo)

    return round(valor * factor, 2)



# Leer TXT
df = pd.read_csv(ruta,sep=";",low_memory=False)

# Convertir P21 a número
df["P21"] = pd.to_numeric(df["P21"],errors="coerce")


# Filtrar aglomerados
df = df[df["AGLOMERADO"].isin([33,13])]


# Crear P21 actualizado
df = df.assign(P21Actualizado=df["P21"].apply(lambda x: actualizar_p21(x, periodo_archivo)))


# Guardar
df.to_csv(rutaGuardado,sep=";",index=False,float_format="%.2f")

print("Proceso terminado y archivo guardado. Ruta Guardado: ", rutaGuardado)