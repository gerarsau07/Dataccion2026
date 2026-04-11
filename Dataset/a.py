import pandas as pd
import json

# 1. Cargamos ambos archivos
df_mat = pd.read_json('grafica_comparativa_paises.json')
df_egr = pd.read_json('egreso_mujeres_stem.json')

# 2. Obtenemos el último año de cada país para Matrícula
df_mat_latest = df_mat.sort_values('Anio').groupby('Pais').tail(1).copy()
df_mat_latest = df_mat_latest.rename(columns={'Mujeres': 'Matricula_Mujeres'})

# 3. Obtenemos el último año de cada país para Egreso
df_egr_latest = df_egr.sort_values('year').groupby('País__ESTANDAR').tail(1).copy()
df_egr_latest = df_egr_latest.rename(columns={'Mujeres_Egresadas': 'Egreso_Mujeres', 'País__ESTANDAR': 'Pais'})

# 4. Unimos todo en una sola super-tabla
df_mapa = pd.merge(df_mat_latest[['Pais', 'Matricula_Mujeres']], 
                   df_egr_latest[['Pais', 'Egreso_Mujeres']], 
                   on='Pais', how='inner')

# 5. EL TRUCO ESTRELLA: Diccionario de traducción para react-simple-maps
traduccion = {
    'Argentina': 'Argentina', 'Belice': 'Belize', 'Brasil': 'Brazil', 'Chile': 'Chile', 
    'Colombia': 'Colombia', 'Costa Rica': 'Costa Rica', 'Cuba': 'Cuba', 
    'República Dominicana': 'Dominican Republic', 'Ecuador': 'Ecuador', 'Santa Lucía': 'Saint Lucia', 
    'México': 'Mexico', 'Nicaragua': 'Nicaragua', 'Panamá': 'Panama', 
    'El Salvador': 'El Salvador', 'Trinidad y Tabago': 'Trinidad and Tobago', 'Uruguay': 'Uruguay'
}

df_mapa['Mapa_Name'] = df_mapa['Pais'].map(traduccion)

# Redondeamos y exportamos
df_mapa = df_mapa.round(2)
nombre_archivo = 'mapa_datos_unificados.json'
df_mapa.to_json(nombre_archivo, orient='records')

print(f"¡Listo! Archivo {nombre_archivo} creado exitosamente.")