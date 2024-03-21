def unit_price(load_forecast):
    if load_forecast < 0.4:
        return 7
    elif 0.4 <= load_forecast < 0.5:
        return 8
    elif 0.5 <= load_forecast <= 0.699:
        return 9
    elif 0.7 <= load_forecast <= 1.0000:
        return 10
    else:
        return 11