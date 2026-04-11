# Datacción 2026: Pipeline de Datos y Análisis Predictivo ("El Filtro Invisible")

Este repositorio contiene la arquitectura de procesamiento de datos, análisis exploratorio y modelos de Machine Learning desarrollados para evaluar la retención de talento femenino en áreas STEM y su impacto directo en el crecimiento económico (PIB) de la región latinoamericana.

El enfoque central de este trabajo es la consolidación de múltiples fuentes de datos socioeconómicos para visibilizar el "Filtro Invisible": la brecha sistémica que impide que las mujeres transiten desde la educación superior hasta los puestos de liderazgo, y la simulación matemática del costo de oportunidad que esto representa.

## Diccionario y Fuentes de Datos

Para garantizar la reproducibilidad y transparencia del análisis, todos los conjuntos de datos utilizados provienen de fuentes oficiales e instituciones internacionales reconocidas. A continuación, se detalla el origen y propósito de cada dataset procesado en nuestro pipeline ETL:

| Archivo / Dataset | Descripción del Contenido | Fuente Oficial | Enlace de Consulta |
| :--- | :--- | :--- | :--- |
| **`Matriculación y Egreso STEM`** | Datos históricos (2015-2025) del porcentaje de mujeres matriculadas y graduadas en educación terciaria para LatAm y el Caribe. | Instituto de Estadística de la UNESCO (UIS) | [UNESCO Data Browser: Education OPRI](https://databrowser.uis.unesco.org/view#ndicatorPaths=UIS-EducationOPRI%3A0%3AFGP.5T8.F500600700&geoMode=countries&geoUnits=ARG%2CABW%2CBRB%2CBLZ%2CBRA%2CVGB%2CCYM%2CCHL%2CCOL%2CCRI%2CCUB%2CDOM%2CECU%2CSLV%2CGRD%2CGTM%2CGUY%2CHND%2CMEX%2CNIC%2CPAN%2CPER%2CPRI%2CLCA%2CSXM%2CTTO%2CTCA%2CURY%2CVEN&browsePath=EDUCATION%2FUIS-EducationOPRI%2Fgraduates&timeMode=range&view=table&chartMode=multiple&tableIndicatorId=FGP.5T8.F500600700&chartIndicatorId=FGP.5T8.F500600700) |
| **`tiempo_trabajoRemunerado.csv`** | Distribución de horas dedicadas al trabajo no remunerado (cuidados y hogar) vs. trabajo remunerado, desglosado por sexo y país. | CEPAL / ONU Mujeres | [Base de Datos CEPALSTAT](https://statistics.cepal.org/portal/cepalstat/index.html?lang=es) |
| **`PuestosDirectivos.csv`** | Evolución histórica del porcentaje de participación femenina en posiciones de liderazgo y gerencia media/alta corporativa. | OIT (Organización Internacional del Trabajo) | [ILOSTAT Data Explorer](https://ilostat.ilo.org/es/data/) |
| **`Poblacion.csv`** | Demografía general histórica proyectada, escalada en millones de habitantes, segmentada por país y género. | Banco Mundial | [World Bank Open Data: Población](https://data.worldbank.org/indicator/SP.POP.TOTL) |
| **`dataPBI.csv`** | Tasas de crecimiento económico anual y Producto Interno Bruto histórico para los países analizados. | Banco Mundial | [World Bank Open Data: Crecimiento PIB](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG) |
| **`Salarios.csv`** | Relación de la brecha salarial y el cálculo de eficiencia o retorno educativo (Salario vs. Años de estudio). | OIT / Foro Económico Mundial | [Global Gender Gap Report (WEF)](https://www.weforum.org/publications/global-gender-gap-report-2023/) |

> **Nota sobre el procesamiento:** Los datos crudos extraídos de estas fuentes fueron sometidos a un proceso de estandarización (renombramiento de columnas, eliminación de espacios, manejo de nulos) mediante Python/Pandas para consolidarlos en el `df_master` utilizado por nuestro modelo predictivo.

## Pipeline de Procesamiento (ETL)

Para unificar los datos en un `DataFrame` maestro (`df_master`), se implementó un pipeline de limpieza y estandarización robusto:

1. **Estandarización de Variables Llave:** Normalización de los nombres de columnas de tiempo (`Anio`, `year`, `time` unificados a `Anios`) y segmentación demográfica (`sex.item` unificado a `Sexo`).
2. **Limpieza de Cadenas (Strings):** Remoción de espacios en blanco ocultos en las variables categóricas (ej. nombres de los países) para garantizar la integridad de los *Joins*.
3. **Conversión de Unidades:** Escalamiento de la métrica de población (multiplicación por 1,000) para reflejar cifras reales.
4. **Fusión de Datos (Data Merging):** Integración de datasets mediante cruces relacionales (`pd.merge`) utilizando `Pais`, `Anios` y `Sexo` como llaves primarias.
5. **Manejo de Valores Nulos (Imputación):** Aplicación de técnicas `ffill()` y `bfill()` en el dataset maestro para mantener la continuidad de las series de tiempo. Uso de limpiezas estrictas (`dropna`) exclusivas para los conjuntos de entrenamiento para evitar introducir ruido en los algoritmos predictivos.

## Modelado Predictivo 

En lugar de utilizar proyecciones de tiempo univariadas, se implementó un modelo multivariable para medir el impacto real de la equidad de género en la economía.

* **Algoritmo:** Regresión Lineal con Regularización (`Ridge` de Scikit-Learn).
* **Variables Independientes (Features):** `Anios` y `Porcentaje_Directivas`.
* **Variable Dependiente (Target):** Índice Acumulado del Crecimiento del PIB.
* **Proyección (2030 - 2050):** El simulador proyecta el futuro basándose en tres escenarios matemáticos:
  1. **Escenario Inercial:** El modelo asume que las brechas actuales se mantienen congeladas.
  2. **Progreso Lento:** Simulador con un incremento marginal (5%) en equidad directiva.
  3. **Meta ODS 2030:** Simulador que proyecta el alcance de la paridad directiva (50%) acoplado a un factor acelerador de crecimiento económico.

## Archivos de Salida 

El pipeline de Python está diseñado para procesar la información y generar archivos estáticos optimizados (`.json`) para ser consumidos por el Frontend (React/Next.js). Los principales *outputs* generados son:

* `impacto_mujeres.json`: Datos consolidados para análisis cuatridimensional (Tiempo Remunerado vs. Retorno Educativo vs. Brecha Salarial).
* `prediccion_filtro_invisible_2100.json`: Proyecciones Ridge históricas y futuras por país para matrícula y puestos directivos.
* `simulacion_ods_pib.json`: Series de tiempo resultantes del simulador de los 3 escenarios económicos hacia el año 2030.
* `mapa_matriculacion.json`: Consolidado geográfico para el despliegue del mapa de calor de retención de talento.

## Stack Tecnológico de Datos

* **Lenguaje:** Python 3.12+
* **Manipulación y Análisis:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (`Ridge`, `LinearRegression`)
* **Visualización de Validación:** Plotly (`plotly.express`, `plotly.graph_objects`)

##  Equipo de Desarrollo

Este proyecto fue desarrollado y estructurado por:

* Gudelia Pilar Pérez Conde
* Gerardo Saucedo Pérez
* Jorge Eduardo Berber Carretero
* Luis Fernando Romero Coyotecatl