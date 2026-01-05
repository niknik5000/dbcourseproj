import random
from datetime import datetime, timedelta
from pathlib import Path

# set output path to script folder
script_dir = Path(__file__).resolve().parent
filename = script_dir / "NEWflights.txt"

# flight generation parameters
total_flights = 3000  
start_date = datetime(2024, 1, 1, 0, 0, 0)
end_date = datetime(2027, 1, 31, 23, 59, 59)
total_days = (end_date - start_date).days

# airport pools for each region
greece_hub = ['ATH', 'SKG']
greece_islands = ['HER', 'CHQ', 'RHO', 'JTR', 'JMK', 'CFU', 'ZTH', 'KGS', 'LXS', 'AXD', 'SMI', 'JSI', 'EFL', 'IOA', 'KLX']
europe_hubs = ['LHR', 'FRA', 'CDG', 'AMS', 'MUC', 'MAD', 'FCO', 'IST', 'ZRH', 'VIE']
europe_cities = ['MAN', 'EDI', 'DUB', 'ORY', 'NCE', 'BRU', 'BER', 'GVA', 'MXP', 'VCE', 'BCN', 'AGP', 'LIS', 'OPO', 'CPH', 'ARN', 'OSL', 'HEL', 'WAW', 'PRG', 'BUD', 'OTP', 'SOF', 'BEG']
usa_hubs = ['JFK', 'EWR', 'ORD', 'ATL', 'LAX', 'SFO', 'DFW', 'MIA']
usa_cities = ['BOS', 'IAD', 'PHL', 'MCO', 'DTW', 'MSP', 'SEA', 'LAS', 'PHX', 'DEN', 'IAH']
asia_hubs = ['DXB', 'DOH', 'SIN', 'BKK', 'HKG', 'HND', 'ICN', 'PEK', 'PVG']
australia = ['SYD', 'MEL', 'AKL']

# airline mapping with codes
airlines = {
    1: {'name': 'Aegean Airlines', 'code': 'A3'},
    2: {'name': 'Sky Express', 'code': 'GQ'},
    3: {'name': 'United Airlines', 'code': 'UA'},
    4: {'name': 'Ryanair', 'code': 'FR'},
    5: {'name': 'Emirates', 'code': 'EK'},
    6: {'name': 'Delta Airlines', 'code': 'DL'},
    7: {'name': 'Air France', 'code': 'AF'},
    8: {'name': 'Lufthansa', 'code': 'LH'},
    9: {'name': 'British Airways', 'code': 'BA'},
    10: {'name': 'Qatar Airways', 'code': 'QR'},
}

# generate flights list
generated_flights = []
flight_counter = 1000

for _ in range(total_flights):
    # pick random scenario with weights
    scenario = random.choices(
        ['GR_INTERNAL', 'EU_INTERNAL', 'GR_EU', 'US_INTERNAL', 'LONG_HAUL'], 
        weights=[30, 25, 20, 15, 10], 
        k=1
    )[0]

    origin, dest, airline_id, plane_id, duration = "", "", 0, 0, 0

    # greece domestic flights
    if scenario == 'GR_INTERNAL':
        origin = random.choice(greece_hub)
        dest = random.choice(greece_islands)
        if random.random() > 0.5: origin, dest = dest, origin
        airline_id = random.choice([1, 2])
        plane_id = random.choice([1, 2, 3]) 
        duration = random.randint(35, 60)
        base_price = random.randint(40, 100)

    # europe internal flights
    elif scenario == 'EU_INTERNAL':
        origin = random.choice(europe_hubs)
        dest = random.choice(europe_cities)
        if random.random() > 0.5: origin, dest = dest, origin
        airline_id = random.choice([4, 7, 8, 9])
        plane_id = random.choice([3, 4, 5]) 
        duration = random.randint(90, 180)
        base_price = random.randint(60, 200)

    # greece to europe
    elif scenario == 'GR_EU':
        origin = random.choice(greece_hub)
        dest = random.choice(europe_hubs)
        if random.random() > 0.5: origin, dest = dest, origin
        airline_id = random.choice([1, 4, 8, 9]) 
        plane_id = random.choice([3, 4, 5])
        duration = random.randint(150, 240)
        base_price = random.randint(100, 300)

    # us domestic flights
    elif scenario == 'US_INTERNAL':
        origin = random.choice(usa_hubs)
        dest = random.choice(usa_cities)
        if random.random() > 0.5: origin, dest = dest, origin
        airline_id = random.choice([3, 6])
        plane_id = random.choice([5, 4])
        duration = random.randint(120, 300)
        base_price = random.randint(150, 450)

    # long haul flights
    elif scenario == 'LONG_HAUL':
        # combine all major hubs
        hubs = europe_hubs + usa_hubs + asia_hubs + australia
        origin = random.choice(hubs)
        dest = random.choice(hubs)
        while origin == dest: dest = random.choice(hubs)
        airline_id = random.choice([5, 6, 8, 9, 10])
        plane_id = random.choice([6, 7, 8, 9, 10])
        duration = random.randint(400, 900)
        base_price = random.randint(500, 1600)

    # generate random departure time
    rand_day = random.randint(0, total_days)
    rand_sec = random.randint(0, 86400)
    dep_dt = start_date + timedelta(days=rand_day, seconds=rand_sec)
    arr_dt = dep_dt + timedelta(minutes=duration)

    # summer surge pricing
    if dep_dt.month in [6, 7, 8]:
        base_price = base_price * 1.4
    
    final_price = round(base_price, 2)

    # format times and gate
    dep_str = dep_dt.strftime('%Y-%m-%d %H:%M')
    arr_str = arr_dt.strftime('%Y-%m-%d %H:%M')
    gate = f"{random.choice(['A','B','C','D'])}{random.randint(1,40)}"

    # build flight number from airline code
    code = airlines.get(airline_id, {}).get('code', 'FL')
    flight_num = f"{code}{flight_counter:04d}"
    flight_counter += 1

    # get airline name for lookup
    airline_name = airlines[airline_id]['name']
    
    # build sql insert statement
    sql = (
        f"INSERT INTO pthsh (arithmos_pthshs, etairia_id, aeroplano_id, "
        f"aerodromio_anaxwrhshs_id, aerodromio_afikshs_id, wra_anaxwrhshs, wra_afikshs, pulh, vasikh_timh) "
        f"VALUES ('{flight_num}', (SELECT etairia_id FROM etairia WHERE onoma='{airline_name}'), {plane_id}, "
        f"(SELECT aerodromio_id FROM aerodromio WHERE kwdikos='{origin}'), "
        f"(SELECT aerodromio_id FROM aerodromio WHERE kwdikos='{dest}'), "
        f"'{dep_str}', '{arr_str}', '{gate}', {final_price});"
    )
    
    generated_flights.append((dep_dt, sql))

# sort flights by departure time
generated_flights.sort(key=lambda x: x[0])

# write all flights to file
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"-- ΑΥΤΟΜΑΤΗ ΔΗΜΙΟΥΡΓΙΑ {total_flights} ΠΤΗΣΕΩΝ ΜΕ 150 ΑΕΡΟΔΡΟΜΙΑ\n")
    f.write("-- Καλύπτει περιόδους 2024-2027\n\n")
    for _, sql in generated_flights:
        f.write(sql + "\n")
   

print("DONE")