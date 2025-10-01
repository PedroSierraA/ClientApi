from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Cargar CSV al iniciar
df = pd.read_csv("creditos_dummy.csv", dtype=str)
df["nombre_norm"] = df["nombre persona"].str.strip().str.lower()
df["id_norm"] = df["id"].astype(str).str.strip()

class ClienteRequest(BaseModel):
    nombre: str
    identificacion: str

@app.get("/")
def root():
    return {"status": "ok", "message": "DummyClient API está corriendo"}

@app.post("/buscar_cliente")
def buscar_cliente(req: ClienteRequest):
    nombre = req.nombre.strip().lower()
    identificacion = str(req.identificacion).strip()

    cliente = df[(df["nombre_norm"] == nombre) & (df["id_norm"] == identificacion)]

    if cliente.empty:
        return {"found": False, "cliente": None}

    row = cliente.iloc[0]
    return {
        "found": True,
        "cliente": {
            "nombre": row["nombre persona"],
            "id": str(row["id"]),
            "credit_amount": float(row["credit amount"]),
            "credit_date": row["credit date"],  # string YYYY-MM-DD
            "credit_interest": float(row["credit interest"])
        }
    }
