def buyerSeller(solar_units, storage_units, load_forecast):
    if float(solar_units) + float(storage_units) > float(load_forecast):
        return "Seller"
    else:
        return "Buyer"
    
        