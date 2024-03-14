def buyerSeller(solar_units, storage_units, load_forecast):
    if solar_units + storage_units > load_forecast:
        return "Seller"
    else:
        return "Buyer"
    
        