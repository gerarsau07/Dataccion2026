# Datacción 2026: Pipeline de Datos y Análisis Predictivo ("El Filtro Invisible")

Este repositorio contiene la arquitectura de procesamiento de datos, análisis exploratorio y modelos de Machine Learning desarrollados para evaluar la retención de talento femenino en áreas STEM y su impacto directo en el crecimiento económico (PIB) de la región latinoamericana.

El enfoque central de este trabajo es la consolidación de múltiples fuentes de datos socioeconómicos para visibilizar el "Filtro Invisible": la brecha sistémica que impide que las mujeres transiten desde la educación superior hasta los puestos de liderazgo, y la simulación matemática del costo de oportunidad que esto representa.

##  Fuentes de Datos (Datasets)

El proyecto integra datos de diversas fuentes institucionales, estructurados en las siguientes categorías:

* **Datos de Población y Economía:**
  * `Poblacion.csv`: Demografía histórica por país y sexo.
  * `dataPBI.csv`: Tasas de crecimiento económico anual y PIB.
  * `Salarios.csv`: Retorno educativo y relación salarial.
* **Datos de Brecha y Trabajo:**
  * `tiempo_trabajoRemunerado.csv`: Distribución de carga laboral (remunerada y no remunerada).
  * `PuestosDirectivos.csv`: Porcentaje histórico de participación femenina en posiciones de liderazgo.
  * `data_Proporcion de lugares ocupador por mujeres_FUENTE_CEPAL.csv`: Mujeres Egresadas en carreras STEM.
  

##  Pipeline de Procesamiento (ETL)

Para unificar los datos en un `DataFrame` maestro (`df_master`), se implementó un pipeline de limpieza y estandarización robusto:

1. **Estandarización de Variables Llave:** * Normalización de los nombres de columnas de tiempo (`Anio`, `year`, `time` unificados a `Anios`) y segmentación demográfica (`sex.item` unificado a `Sexo`).
2. **Limpieza de Cadenas (Strings):** * Remoción de espacios en blanco ocultos en las variables categóricas (ej. nombres de los países) para garantizar la integridad de los *Joins*.
3. **Conversión de Unidades:** * Escalamiento de la métrica de población (multiplicación por 1,000) para reflejar cifras reales.
4. **Fusión de Datos (Data Merging):** * Integración de datasets mediante cruces relacionales (`pd.merge`) utilizando `Pais`, `Anios` y `Sexo` como llaves primarias.
5. **Manejo de Valores Nulos (Imputación):** * Aplicación de técnicas `ffill()` y `bfill()` en el dataset maestro para mantener la continuidad de las series de tiempo.
   * Uso de limpiezas estrictas (`dropna`) exclusivas para los conjuntos de entrenamiento (Train sets) para evitar introducir ruido en los algoritmos predictivos.

##  Modelado Predictivo (Machine Learning)

En lugar de utilizar proyecciones de tiempo univariadas, se implementó un modelo multivariable para medir el impacto real de la equidad de género en la economía.

* **Algoritmo:** Regresión Lineal con Regularización (`Ridge` de Scikit-Learn).
* **Variables Independientes (Features):** `Anios` y `Porcentaje_Directivas`.
* **Variable Dependiente (Target):** Índice Acumulado del Crecimiento del PIB.
* **Proyección (2030 - 2050):** El simulador proyecta el futuro basándose en tres escenarios matemáticos:
  1. **Escenario Inercial:** El modelo asume que las brechas actuales se mantienen congeladas.
  2. **Progreso Lento:** Simulador con un incremento marginal (5%) en equidad directiva.
  3. **Meta ODS 2030:** Simulador que proyecta el alcance de la paridad directiva (50%) acoplado a un factor acelerador de crecimiento económico.

## Archivos de Salida (Data Exports)

El pipeline de Python está diseñado para procesar la información y generar archivos estáticos optimizados (`.json`) para ser consumidos por el Frontend (React/Next.js). Los principales *outputs* generados son:

* `impacto_mujeres.json`: Datos consolidados para análisis cuatridimensional (Tiempo Remunerado vs. Retorno Educativo vs. Brecha Salarial).
* `prediccion_filtro_invisible_2100.json`: Proyecciones Ridge históricas y futuras por país para matrícula y puestos directivos.
* `simulacion_ods_pib.json`: Series de tiempo resultantes del simulador de los 3 escenarios económicos hacia el año 2030.
* `grafica_comparativa_paises.json`: Consolidado geográfico para el despliegue del mapa de calor de retención de talento.

## 🛠️ Stack Tecnológico de Datos

* **Lenguaje:** Python 3.12+
* **Manipulación y Análisis:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (`Ridge`, `LinearRegression`)
* **Visualización de Validación:** Plotly (`plotly.express`, `plotly.graph_objects`)