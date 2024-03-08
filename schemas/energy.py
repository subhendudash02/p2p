from pydantic import BaseModel

class EnergyData(BaseModel):
    storageUnits: float
    loadForecast: float
    profitPref: float