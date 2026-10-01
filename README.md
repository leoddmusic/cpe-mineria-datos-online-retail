# CPE Minería de Datos — Online Retail

## Predicción semanal de demanda observada por producto

Proyecto del Componente Práctico-Experimental de **Minería de Datos (UEA-L-UFPTI-009-A)**.

### Objetivo
Analizar las transacciones históricas del dataset Online Retail y comparar modelos de regresión para estimar unidades vendidas observadas por producto y semana.

### Dataset
- Fuente: UCI Machine Learning Repository — Online Retail.
- Registros originales: 541.909.
- Periodo: diciembre de 2010 a diciembre de 2011.
- Copia utilizada: `datos/Online Retail.xlsx`.

### Pipeline
1. Validación de estructura del archivo.
2. Eliminación de 5.268 duplicados exactos.
3. Identificación de cancelaciones mediante `InvoiceNo`.
4. Selección de ventas positivas de productos.
5. Agregación a unidad producto-semana.
6. Construcción de semanas internas sin ventas con demanda 0.
7. Feature engineering sin fuga temporal.
8. División temporal 38 semanas entrenamiento / 10 prueba.
9. Comparación de Regresión Lineal, Árbol de Decisión y Random Forest.
10. Validación cruzada temporal con 5 particiones.
11. Evaluación con MAE, RMSE y R².
12. Exportación del Random Forest seleccionado a `.pkl`.
13. Exposición del modelo mediante API FastAPI y web app mínima.

### Variables derivadas
`DemandLag1`, `DemandLag2`, `DemandRolling4`, `InvoiceCountLag1`, `WeekSin`, `WeekCos`.

### Resultados de prueba
| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| Random Forest | 38.88 | 134.34 | 0.344 |
| Árbol de Decisión | 39.93 | 142.64 | 0.261 |
| Baseline Lag1 | 40.89 | 149.59 | 0.187 |
| Regresión Lineal | 40.92 | 130.31 | 0.383 |

Random Forest se conserva como modelo principal por menor MAE y mayor estabilidad en validación cruzada temporal. Regresión Lineal obtuvo mejor RMSE y R² en el test final, pero mostró variabilidad mayor entre folds.

### Estructura del repositorio
```text
README.md
requirements.txt
VALIDACION_REAL.json
datos/
  Online Retail.xlsx
notebooks/
  CPE_Online_Retail_Final_API_WEB.ipynb
modelo/
  modelo_random_forest_demanda.pkl
api/
  app.py
web/
  index.html
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

### Ejecutar API
```powershell
pip install -r requirements.txt
python -m uvicorn api.app:app --reload --host 127.0.0.1 --port 8000
```

Documentación interactiva: `http://127.0.0.1:8000/docs`.

### Ejecutar web app
Desde la raíz del repositorio:
```powershell
python -m http.server 5500 --directory web
```

Abrir `http://127.0.0.1:5500`.

### Limitación principal
La variable objetivo representa **demanda observada como unidades vendidas**. El dataset no incluye inventario disponible ni faltantes, por lo que no permite estimar demanda latente no satisfecha.
