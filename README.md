# DummyClient API

API simple en FastAPI para consultar clientes en mora desde un CSV.  
Diseñada para integrarse con un agente en Vapi a través de HTTP Tool.

## Endpoints

- **GET /** → prueba de estado
- **POST /buscar_cliente?nombre=<nombre>&identificacion=<id>**
  - Busca un cliente por nombre e identificación.
  - Respuesta:
    ```json
    {
      "found": true,
      "cliente": {
        "nombre": "Pedro Sierra",
        "id": "87654321",
        "credit_amount": 2500.0,
        "credit_date": "2025-08-30",
        "credit_interest": 3.0
      }
    }
    ```

## Despliegue en Railway

1. Subir repo a GitHub.
2. En Railway → **New Project** → **Deploy from GitHub Repo**.
3. Railway detectará `Procfile` y levantará el servicio automáticamente.
4. Obtendrás un dominio público tipo `https://dummyclient.up.railway.app`.
