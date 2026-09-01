# CPE Minería de Datos - Online Retail

## Predicción semanal de demanda observada por producto

Proyecto del Componente Práctico-Experimental de **Minería de Datos (UEA-L-UFPTI-009-A)**.

### Objetivo
Analizar las transacciones históricas del dataset Online Retail y comparar modelos de regresión para estimar unidades vendidas observadas por producto y semana.

### Dataset
- Fuente: UCI Machine Learning Repository - Online Retail
- URL: https://archive.ics.uci.edu/dataset/352/online+retail
- Registros originales: 541,909
- Periodo: diciembre de 2010 a diciembre de 2011
- El archivo `Online Retail.xlsx` **no se incluye** en el repositorio; debe descargarse desde UCI.

### Pipeline
1. Validación de estructura del archivo.
2. Eliminación de 5,268 duplicados exactos.
3. Identificación de cancelaciones mediante `InvoiceNo`.
4. Selección de ventas positivas de productos.
5. Agregación a unidad producto-semana.
6. Construcción de semanas internas sin ventas con demanda 0.
7. Feature engineering sin fuga temporal.
8. División temporal 38 semanas de entrenamiento / 10 de prueba.
9. Comparación de Regresión Lineal, Árbol de Decisión y Random Forest.
10. Validación cruzada temporal con 5 particiones.
11. Evaluación con MAE, RMSE y R².

### Variables derivadas
`DemandLag1`, `DemandLag2`, `DemandRolling4`, `InvoiceCountLag1`, `WeekSin`, `WeekCos`.

### Resultados de prueba
| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| Random Forest | 38.88 | 134.34 | 0.344 |
| Árbol de Decisión | 39.93 | 142.64 | 0.261 |
| Baseline Lag1 | 40.89 | 149.59 | 0.187 |
| Regresión Lineal | 40.92 | 130.31 | 0.383 |

Random Forest se considera el modelo principal por menor MAE y mayor estabilidad en validación cruzada temporal. La Regresión Lineal obtuvo mejor RMSE y R² en el test final, pero mostró variabilidad mucho mayor entre folds.

### Reproducibilidad
Abra el notebook en Google Colab, ejecute todas las celdas y seleccione `Online Retail.xlsx` cuando se solicite.

```bash
pip install pandas numpy matplotlib scikit-learn openpyxl
```

### Estructura recomendada del repositorio
```text
README.md
requirements.txt
notebooks/
  CPE_Online_Retail_Final.ipynb
resultados/
  comparacion_modelos.csv
  metricas_test.csv
  validacion_cruzada_resumen.csv
  resumen_paso6.json
figuras/
  comparacion_mae_rmse.png
  demanda_semanal_test.png
  importancia_random_forest.png
```

### Limitación principal
El objetivo representa **demanda observada como unidades vendidas**. El dataset no incluye inventario disponible ni faltantes, por lo que no permite estimar demanda latente no satisfecha.
