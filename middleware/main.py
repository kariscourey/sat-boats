import uvicorn

from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Model load --------------------------------------------------------------------

model_output = [
    {
        "vessel_name": "OOCL Malaysia",
        "mmsi": "477220100",
        "predicted_locations": [
            {
                "base_date_time": datetime(2024, 2, 8, 12, 30, 0).astimezone(
                    timezone.utc
                ),
                "coordinates": [
                    {
                        "lat": 21.2775,
                        "lon": -157.8226,
                        "probability": 0.91,
                    },
                    {
                        "lat": 21.1775,
                        "lon": -157.7226,
                        "probability": 0.86,
                    },
                    {
                        "lat": 21.3775,
                        "lon": -157.3226,
                        "probability": 0.61,
                    },
                ],
            },
        ],
    },
    {
        "vessel_name": "BOW Canada",
        "mmsi": "819101222",
        "predicted_locations": [
            {
                "base_date_time": datetime(2024, 3, 10, 11, 12, 0).astimezone(
                    timezone.utc
                ),
                "coordinates": [
                    {
                        "lat": 23.1001,
                        "lon": -159.2000,
                        "probability": 0.53,
                    },
                    {
                        "lat": 23.9019,
                        "lon": -159.1201,
                        "probability": 0.31,
                    },
                    {
                        "lat": 21.9995,
                        "lon": -156.4387,
                        "probability": 0.12,
                    },
                ],
            },
        ],
    },
]


# FastAPI app configs -----------------------------------------------------------


# define pydantic models
class ShipOut(BaseModel):

    ship: dict


class ShipsOut(BaseModel):

    ships: list


# instantiate fastapi app
app = FastAPI(title="API", description="API")

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# FastAPI app endpoints ---------------------------------------------------------


@app.get("/api/ships/{ship_mmsi}/")
def get_ship(ship_mmsi: str) -> ShipOut:
    return ShipOut(ship=model_output[0])


@app.get("/ships")
def get_ships() -> ShipsOut:

    # return
    return ShipsOut(ships=model_output)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info", reload=False)
