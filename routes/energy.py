from fastapi import APIRouter, Depends, HTTPException
from schemas.energy import *
from auth.status import is_logged_in
from db.operations import read_all, read, update
from db.models import energy_table
from db.auth import get_current_user, get_user_id
import csv
from algorithm import unit_price, algo

energy_router = APIRouter(prefix="/energy", tags=["energy"])

@energy_router.post("/x")
def create_energy(item: EnergyData, check: bool = Depends(is_logged_in)):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    current_user = get_current_user()
    new_item = item.dict()
    new_item["username"] = current_user
    new_item["ratingPref"] = round(1 - new_item["profitPref"], 2)

    get_solar_units = read(energy_table, current_user)

    new_item["total"] = round(float(new_item["storageUnits"]) + float(get_solar_units[6]), 2)

    rename_dict = {
        "Storage": new_item["storageUnits"],
        "Load Forecast (Units)": new_item["loadForecast"],
        "Total (Units)": new_item["total"],
        "Profit_pref": new_item["profitPref"],
        "Rating_pref": new_item["ratingPref"],
    }

    update(energy_table, get_user_id(current_user), rename_dict)

    return {
        "username": current_user,
        "status": "uploaded"
    }

@energy_router.get("/x")
def read_energy(check: bool = Depends(is_logged_in)):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    current_user = get_current_user()
    values = read(energy_table, current_user)
    return {
        "username": current_user,
        "storageUnits": values[2],
        "loadForecast": values[3],
        "profitPref": values[4],
        "ratingPref": values[5],
        "solarUnits": values[6]
    }

@energy_router.get("/run")
def run_algo():
    outfile = open("algorithm/data.csv", "w")
    read_energy = read_all(energy_table)

    with open("algorithm/data.csv", 'w', newline='') as out_file:
        outcsv = csv.writer(out_file)
        outcsv.writerow(["Prosumer_Id", "username", "Storage", "Load Forecast (Units)", "Profit_pref", "Rating_pref", "Solar", "Total (Units)", "Period (Hr)", "Unit Price", "DSM"])
        for rows in read_energy:
            unit = unit_price.unit_price(float(rows[3]))
            outcsv.writerow(tuple(rows) + (1, ) + (unit, ) + (0,))
    
    algo.algo()

    outfile.close()
    return {
        "status": "running"
    }

@energy_router.get("/result")
def get_result():
    with open("D:\\Programming\\p2p\\result_transactions.csv") as csvfile:
        line = csv.reader(csvfile)
        result = []
        for i in line:
            result.append(i)
    return {"res": result}