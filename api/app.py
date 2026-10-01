from __future__ import annotations

import math
import os
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

FEATURES = [
    "DemandLag1",
    "DemandLag2",
    "DemandRolling4",
    "InvoiceCountLag1",
    "WeekSin",
    "WeekCos",
]

DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[1] / "modelo" / "modelo_random_forest_demanda.pkl"
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH)))

app = FastAPI(
    title="API de predicción de demanda semanal - Online Retail",
    version="1.0.0",
    description=(
        "API académica del CPE de Minería de Datos. Usa el Random Forest validado "
        "para estimar demanda observada semanal de un producto."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

_model = None

class PredictionInput(BaseModel):
    demand_lag1: float = Field(ge=0, description="Demanda observada de la semana anterior")
    demand_lag2: float = Field(ge=0, description="Demanda observada de dos semanas atrás")
    demand_rolling4: float = Field(ge=0, description="Promedio de demanda de las cuatro semanas anteriores")
    invoice_count_lag1: float = Field(ge=0, description="Número de facturas del producto en la semana anterior")
    week_number: int = Field(ge=1, le=53, description="Número ISO de la semana del año")

def load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo en {MODEL_PATH}. "
                "Ejecute el notebook final y copie el archivo .pkl generado a la carpeta modelo/."
            )
        _model = joblib.load(MODEL_PATH)
    return _model

@app.get("/")
def root():
    return {
        "proyecto": "CPE Minería de Datos - Online Retail",
        "modelo": "Random Forest",
        "objetivo": "Predicción de demanda observada semanal por producto",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {
        "status": "ok" if MODEL_PATH.exists() else "modelo_pendiente",
        "model_exists": MODEL_PATH.exists(),
    }

@app.post("/predict")
def predict(data: PredictionInput):
    try:
        model = load_model()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    week_sin = math.sin(2 * math.pi * data.week_number / 52.0)
    week_cos = math.cos(2 * math.pi * data.week_number / 52.0)

    row = pd.DataFrame([[data.demand_lag1, data.demand_lag2, data.demand_rolling4,
                         data.invoice_count_lag1, week_sin, week_cos]], columns=FEATURES)

    prediction = max(float(model.predict(row)[0]), 0.0)

    return {
        "predicted_demand_units": round(prediction, 2),
        "model": "Random Forest",
        "week_number": data.week_number,
        "interpretation": "Estimación de unidades vendidas observadas; no representa demanda latente no satisfecha.",
    }
