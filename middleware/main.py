import uvicorn
import pandas as pd

from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Model load --------------------------------------------------------------------

data = {
    "VesselName": [
        "OOCL Malaysia",
        "BOW Canada",
        "BOW Canada",
        "BOW Canada",
    ],
    "MMSI": ["12309821", "23157653", "23157653", "23157653"],
    "BaseDateTime": [
        datetime(2024, 2, 8, 12, 30, 0).astimezone(timezone.utc),
        datetime(2024, 2, 8, 12, 30, 0).astimezone(timezone.utc),
        datetime(2024, 2, 7, 12, 30, 0).astimezone(timezone.utc),
        datetime(2024, 2, 6, 12, 30, 0).astimezone(timezone.utc),
    ],
    "LAT": ["20.12321", "21.97984", "23.19092", "21.97984"],
    "LON": ["158.9781", "159.97984", "160.23101", "158.9781"],
    "Probability": [0.871, 0.7612, 0.9999, 0.12908],
}

df = pd.DataFrame(data)


# FastAPI app configs -----------------------------------------------------------


# define pydantic models


class ShipOut(BaseModel):

    predictions: list


class ShipsOut(BaseModel):

    predictions: list


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
async def get_ship(ship_mmsi: str):

    # get specific ship
    filt_df = df[df["MMSI"] == ship_mmsi]

    # get most recent basedatetime (one data point), filter to only get those probabilities
    most_recent = filt_df["BaseDateTime"].max()
    filt_df = filt_df[filt_df["BaseDateTime"] == most_recent]

    # convert to outputable format
    predictions = []

    for _, row in filt_df.iterrows():
        prediction = {
            "vessel_name": row["VesselName"],
            "mmsi": row["MMSI"],
            "base_date_time": row["BaseDateTime"],
            "lat": row["LAT"],
            "lon": row["LON"],
            "probability": row["Probability"],
        }
        predictions.append(prediction)

    return ShipOut(predictions=predictions)


@app.get("/api/ships/")
async def get_ships():

    # # get unique mmsi (unnecessary?)
    # mmsis = df["MMSI"].unique()

    # get most recent data point for each MMSI
    filt_df = df.loc[df.groupby("MMSI")["BaseDateTime"].idxmax()]

    # convert to outputable format
    predictions = []

    for _, row in filt_df.iterrows():
        prediction = {
            "vessel_name": row["VesselName"],
            "mmsi": row["MMSI"],
            "base_date_time": row["BaseDateTime"],
            "lat": row["LAT"],
            "lon": row["LON"],
            # "probability": row["Probability"], # don't care about prob here
        }
        predictions.append(prediction)

    return ShipsOut(predictions=predictions)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info", reload=False)
