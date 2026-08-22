import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("graficos", exist_ok=True)
sns.set_theme(style="whitegrid")


# ─────────────────────────────────────────── CARGA DE DATOS ───────────────────────────────────────────
tasas = pd.read_csv("resultados/tasas.csv")
ingresos = pd.read_csv("resultados/ingresos.csv")
ing_sexo = pd.read_csv("resultados/ing_sexo.csv")
ing_educativo = pd.read_csv("resultados/ing_educativo.csv")
ing_calif = pd.read_csv("resultados/ing_calif.csv")
ing_edad = pd.read_csv("resultados/ing_edad.csv")
ing_rama = pd.read_csv("resultados/ing_rama.csv")

tasas = tasas.sort_values(["AGLOMERADO", "PERIODO"])
tasas_13 = tasas[tasas["AGLOMERADO"] == 13].copy().reset_index(drop=True)
tasas_33 = tasas[tasas["AGLOMERADO"] == 33].copy().reset_index(drop=True)

ingresos = ingresos.sort_values(["AGLOMERADO", "PERIODO"])
ing_13 = ingresos[ingresos["AGLOMERADO"] == 13].copy().reset_index(drop=True)
ing_33 = ingresos[ingresos["AGLOMERADO"] == 33].copy().reset_index(drop=True)

periodos = tasas_13["PERIODO"].tolist()
x = range(len(periodos))



# ─────────────────────────────────────────── GRÁFICO 1: Tasa de actividad ─────────────────────────────
periodos_tasas = tasas_13["PERIODO"].tolist()
x_tasas = range(len(periodos_tasas))

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(x_tasas, tasas_13["Tasa actividad"], label="Gran Córdoba (13)", marker="o", markersize=3, color="steelblue")
ax.plot(x_tasas, tasas_33["Tasa actividad"], label="Partidos del GBA (33)", marker="o", markersize=3, color="tomato")
ax.set_title("Evolución de la Tasa de Actividad (2017-2025)", fontsize=14, pad=15)
ax.set_xlabel("Período", fontsize=11)
ax.set_ylabel("Tasa (%)", fontsize=11)
ax.set_xticks(list(x_tasas))
ax.set_xticklabels(periodos_tasas, rotation=90, fontsize=7)
ax.legend(fontsize=10)
ax.set_ylim(30, 70)
plt.tight_layout()
plt.savefig("graficos/tasa_actividad.png", dpi=150)
plt.close()



# ─────────────────────────────────────────── GRÁFICO 2: Tasa de empleo ────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(x_tasas, tasas_13["Tasa empleo"], label="Gran Córdoba (13)", marker="o", markersize=3, color="steelblue")
ax.plot(x_tasas, tasas_33["Tasa empleo"], label="Partidos del GBA (33)", marker="o", markersize=3, color="tomato")
ax.set_title("Evolución de la Tasa de Empleo (2017-2025)", fontsize=14, pad=15)
ax.set_xlabel("Período", fontsize=11)
ax.set_ylabel("Tasa (%)", fontsize=11)
ax.set_xticks(list(x_tasas))
ax.set_xticklabels(periodos_tasas, rotation=90, fontsize=7)
ax.legend(fontsize=10)
ax.set_ylim(30, 70)
plt.tight_layout()
plt.savefig("graficos/tasa_empleo.png", dpi=150)
plt.close()


# ─────────────────────────────────────────── GRÁFICO 3: Tasa de desocupación ─────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(x_tasas, tasas_13["Tasa desocupacion"], label="Gran Córdoba (13)", marker="o", markersize=3, color="steelblue")
ax.plot(x_tasas, tasas_33["Tasa desocupacion"], label="Partidos del GBA (33)", marker="o", markersize=3, color="tomato")
ax.set_title("Evolución de la Tasa de Desocupación (2017-2025)", fontsize=14, pad=15)
ax.set_xlabel("Período", fontsize=11)
ax.set_ylabel("Tasa (%)", fontsize=11)
ax.set_xticks(list(x_tasas))
ax.set_xticklabels(periodos_tasas, rotation=90, fontsize=7)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig("graficos/tasa_desocupacion.png", dpi=150)
plt.close()


# ─────────────────────────────────────────── GRÁFICO 4: Evolucion de ingresos ─────────────────────────────
periodos_ing = ing_13["PERIODO"].tolist()
x_ing = range(len(periodos_ing))

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(x_ing, ing_13["Mediana"], label="Gran Córdoba (13)", marker="o", markersize=3, color="steelblue")
ax.plot(x_ing, ing_33["Mediana"], label="Partidos del GBA (33)", marker="o", markersize=3, color="tomato")
ax.set_title("Evolución de la Mediana de Ingresos Reales (2017-2025)\nEn pesos constantes de 2025_T4", fontsize=13, pad=15)
ax.set_xlabel("Período", fontsize=11)
ax.set_ylabel("Ingreso ($ constantes 2025)", fontsize=11)
ax.set_xticks(list(x_ing))
ax.set_xticklabels(periodos_ing, rotation=90, fontsize=7)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig("graficos/ingresos_mediana.png", dpi=150)
plt.close()



# ─────────────────────────────────────────── GRÁFICO 5: Ingresos por nivel educativo ─────────────────────────────
#tomamos el ultimo trimestre del 2025
ing_educativo = ing_educativo.sort_values(["AGLOMERADO", "PERIODO"])

colores = {
    "Primario incompleto":   "gray",
    "Primario completo":     "steelblue",
    "Secundario incompleto": "orange",
    "Secundario completo":   "green",
    "Superior incompleto":   "tomato",
    "Superior completo":     "purple",
    "Sin instrucción":       "brown"
}

fig, axes = plt.subplots(2, 1, figsize=(16, 12))

for ax, aglo, nombre in zip(axes, [13, 33], ["Gran Córdoba (13)", "Partidos del GBA (33)"]):
    sub = ing_educativo[ing_educativo["AGLOMERADO"] == aglo]
    for nivel, color in colores.items():
        datos = sub[sub["Nivel educativo"] == nivel].reset_index(drop=True)
        if len(datos) > 0:
            ax.plot(datos["Mediana"].values, label=nivel, marker="o", markersize=3, color=color)
    ax.set_title(f"Ingresos por Nivel Educativo — {nombre}", fontsize=11)
    ax.set_xlabel("Período", fontsize=10)
    ax.set_ylabel("Ingreso ($ constantes 2025)", fontsize=10)
    ax.set_xticks(range(len(datos)))
    ax.set_xticklabels(datos["PERIODO"].tolist(), rotation=90, fontsize=7)
    ax.legend(fontsize=9, loc="upper left")

plt.suptitle("Evolución de Ingresos por Nivel Educativo (2017-2025)", fontsize=13)
plt.tight_layout()
plt.savefig("graficos/ingresos_educativo.png", dpi=150)
plt.show()
plt.close()
# ─────────────────────────────────────────── GRÁFICO 5: Ingresos por sexo ─────────────────────────────
#2 graficos lineales por trimestres viendo la evolucion a lo largo del tiempo
ing_sexo = ing_sexo.sort_values(["AGLOMERADO", "PERIODO"])

fig, axes = plt.subplots(1, 2, figsize=(16, 5), sharey=True)

for ax, aglo, nombre in zip(axes, [13, 33], ["Gran Córdoba (13)", "Partidos del GBA (33)"]):
    sub = ing_sexo[ing_sexo["AGLOMERADO"] == aglo]
    for sexo, color in [("Varón", "steelblue"), ("Mujer", "tomato")]:
        datos = sub[sub["Sexo"] == sexo].reset_index(drop=True)
        ax.plot(datos["Mediana"].values, label=sexo, marker="o", markersize=3, color=color)
    ax.set_title(f"Ingresos por Sexo — {nombre}", fontsize=11)
    ax.set_xlabel("Período", fontsize=10)
    ax.set_ylabel("Ingreso ($ constantes 2025)", fontsize=10)
    ax.set_xticks(range(len(datos)))
    ax.set_xticklabels(datos["PERIODO"].tolist(), rotation=90, fontsize=7)
    ax.legend(fontsize=10)

plt.suptitle("Evolución de Ingresos por Sexo (2017-2025)", fontsize=13)
plt.tight_layout()
plt.savefig("graficos/ingresos_sexo.png", dpi=150)
plt.show()
plt.close()
