def create_bus_data(period_data):
    
#                   0   1   2   3    4    5   6   7  8     9
#                 |Bus|Type|Vp|theta|PGi|QGi|PLi|QLi|Qmin|Qmax|
    
    bus_data = []
    
    bus_data.append({'Bus': 1, 'Type': 1, 'Vp': 1, 'theta': 0, 'PGi': 0, 'QGi': 0, 'PLi': 0, 'QLi': 0, 'Qmin': 0, 'Qmax': 0})

    for index, row in period_data.iterrows():
        if row['Category'] == 'B':
            bus_data.append({'Bus': row['Prosumer_Id'], 'Type': 3, 'Vp': 1, 'theta': 0.0, 
                             'PGi': 0, 'QGi': 0, 'PLi': row['Value']*1000*4, 'QLi': 0, 'Qmin': 0, 'Qmax': 0})
        elif row['Category'] == 'S':
            bus_data.append({'Bus': row['Prosumer_Id'], 'Type': 3, 'Vp': 1, 'theta': 0.0, 
                             'PGi': 0, 'QGi': 0, 'PLi': 0, 'QLi': 0, 'Qmin': 0, 'Qmax': 0})
            
    bus_df = pd.DataFrame(bus_data)
    
    return bus_df