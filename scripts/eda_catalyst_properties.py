import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress
import os

# 1. Carga de datos de la Supporting Information con limpieza estricta
ruta_reactividad = os.path.join('data', 'cluster_reactivity_descriptors.csv')
ruta_estructura = os.path.join('data', 'adsorption_structural_descriptors.csv')

df_reactivity = pd.read_csv(ruta_reactividad)
df_structural = pd.read_csv(ruta_estructura)

# Limpiar espacios en blanco que puedan causar un merge incorrecto
df_reactivity['cluster'] = df_reactivity['cluster'].astype(str).str.strip()
df_structural['cluster'] = df_structural['cluster'].astype(str).str.strip()

# Eliminar duplicados potenciales en los archivos origen
df_reactivity = df_reactivity.drop_duplicates(subset=['cluster'])
df_structural = df_structural.drop_duplicates(subset=['cluster'])

# Consolidar los datasets de forma limpia (Inner Join)
df = pd.merge(df_reactivity, df_structural, on='cluster')

# Ingeniería de características automatizada para extraer el número de átomos de Hierro
def extraer_fe(nombre_cluster):
    if nombre_cluster == 'Au6':
        return 0
    if nombre_cluster == 'Fe6':
        return 6
    if 'Fe' in nombre_cluster:
        partes = nombre_cluster.split('Fe')
        if len(partes) > 1 and partes[1] != '':
            return int(partes[1])
        return 1  # Caso Au5Fe (Fe implícito como 1)
    return 0

df['fe_atoms'] = df['cluster'].apply(extraer_fe)

# Ordenar de forma natural por concentración de hierro (de 0 a 6)
df = df.sort_values(by='fe_atoms').reset_index(drop=True)

# Asegurar que los datos para la regresión sean numéricos nativos
df['vea_ev'] = pd.to_numeric(df['vea_ev'])
df['h2o2_freq_cm1'] = pd.to_numeric(df['h2o2_freq_cm1'])

print("✅ Dataset integrado y limpiado exitosamente:")
print(df[['cluster', 'fe_atoms', 'vea_ev', 'h2o2_freq_cm1']])

# 2. CONFIGURACIÓN ESTÉTICA GLOBAL
sns.set_theme(style="ticks", context="talk")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
os.makedirs('outputs', exist_ok=True)

# ==========================================
# 📊 GRÁFICO 1: Matriz de Correlación Limpia (Enfoque H2O2)
# ==========================================
plt.figure(figsize=(9, 7))

columnas_h2o2 = ['fe_atoms', 'vip_ev', 'vea_ev', 'homo_lumo_gap_ev', 
                 'h2o2_d_oo_ang', 'h2o2_freq_cm1']

# SOLUCIÓN: Seleccionar explícitamente solo el subset de columnas numéricas antes del .corr()
df_subset_num = df[columnas_h2o2].apply(pd.to_numeric, errors='coerce')
matriz_corr = df_subset_num.corr()

mask = np.triu(np.ones_like(matriz_corr, dtype=bool))

sns.heatmap(matriz_corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", 
            vmin=-1, vmax=1, square=True, linewidths=0.7, 
            cbar_kws={"shrink": 0.75}, annot_kws={"size": 11, "weight": "bold"})

plt.title(r'Correlation Matrix: $\mathrm{H}_2\mathrm{O}_2$ Activation Descriptors', fontsize=14, weight='bold', pad=20)
plt.tight_layout()
plt.savefig(os.path.join('outputs', 'peroxide_correlation_matrix.png'), dpi=300)
plt.show()

# ==========================================
# 📈 GRÁFICO 2: Regresión Lineal de Activación Cuántica 
# ==========================================
X = df['vea_ev']
Y = df['h2o2_freq_cm1']

slope, intercept, r_value, p_value, std_err = linregress(X, Y)
r_squared = r_value**2

x_line = np.linspace(X.min() - 0.05, X.max() + 0.05, 100)
y_line = slope * x_line + intercept

fig, ax = plt.subplots(figsize=(10, 6))

# Dibujar la línea de tendencia de la regresión lineal
ax.plot(x_line, y_line, color='#e74c3c', linestyle='-', lw=2, 
        label=f'Linear Fit ($R^2 = {r_squared:.3f}$)')

# Paleta indexada de forma segura por el nombre del clúster
paleta_colores = {
    'Au6': '#FFC107', 'Au5Fe': '#FF7043', 'Au4Fe2': '#4CAF50', 
    'Au3Fe3': '#E53935', 'Au2Fe4': '#00BCD4', 'AuFe5': '#E91E63', 'Fe6': '#6A1B9A'
}

# Ciclo de graficado corregido e indexado de forma segura
for i in range(len(df)):
    nombre = df['cluster'].iloc[i]
    color_punto = paleta_colores.get(nombre, '#7f8c8d')
    ax.scatter(X.iloc[i], Y.iloc[i], color=color_punto, s=120, edgecolors='black', zorder=5)
    ax.annotate(f" {nombre}", (X.iloc[i], Y.iloc[i]), fontsize=11, weight='bold', va='center', ha='left', zorder=6)

# Texto matemático con las métricas del modelo
ecuacion_txt = f"$Y = {slope:.2f}X + {intercept:.2f}$\n$R^2 = {r_squared:.3f}$\n$p$-value = {p_value:.4f}"
ax.text(0.05, 0.15, ecuacion_txt, transform=ax.transAxes, fontsize=12,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8f9fa", edgecolor="#dcdde1", alpha=0.9))

ax.set_xlabel('Vertical Electron Affinity (VEA, eV)', fontsize=13, labelpad=10)
ax.set_ylabel(r'$\mathrm{H}_2\mathrm{O}_2$ Stretching Frequency ($\mathrm{cm}^{-1}$)', fontsize=13, labelpad=10)
ax.set_title(r'Backdonation Model: VEA vs. $\mathrm{H}_2\mathrm{O}_2$ Bond Relaxation', fontsize=15, weight='bold', pad=18)
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend(loc='upper right', frameon=True)

plt.tight_layout()
plt.savefig(os.path.join('outputs', 'peroxide_linear_regression.png'), dpi=300)
plt.show()

print("\n" + "="*50)
print("📝 REPORTE ESTADÍSTICO DE LA REGRESIÓN LINEAL")
print("="*50)
print(f"Fórmula: Frecuencia (cm-1) = {slope:.4f} * VEA (eV) + {intercept:.4f}")
print(f"Coeficiente de Determinación (R²): {r_squared:.4f}")
print(f"Significancia Estadística (p-value): {p_value:.5f}")
print("="*50)
