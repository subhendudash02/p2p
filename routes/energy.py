from fastapi import APIRouter, Depends, HTTPException
from schemas.energy import *
from auth.status import is_logged_in
from db.operations import insert
from db.models import energy_table
from db.auth import get_current_user

energy_router = APIRouter(prefix="/energy", tags=["energy"])

@energy_router.post("/x")
def create_energy(item: EnergyData, check: bool = Depends(is_logged_in)):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    new_item = item.dict()
    new_item["username"] = get_current_user()
    insert(energy_table, new_item)

    return {
        "username": get_current_user(),
        "status": "uploaded"
    }