import random
from datetime import datetime, timedelta
from pathlib import Path


# Write output file into the same folder as this script
script_dir = Path(__file__).resolve().parent
filename = script_dir / "NEWflights.txt"
total_flights = 3000  
start_date = datetime(2024, 1, 1, 0, 0, 0)
end_date = datetime(2027, 1, 31, 23, 59, 59)
total_days = (end_date - start_date).days

# HUBs and Cities

greece_hub = ['ATH', 'SKG']
greece_islands = ['HER', 'CHQ', 'RHO', 'JTR', 'JMK', 'CFU', 'ZTH', 'KGS', 'LXS', 'AXD', 'SMI', 'JSI', 'EFL', 'IOA', 'KLX']
europe_hubs = ['LHR', 'FRA', 'CDG', 'AMS', 'MUC', 'MAD', 'FCO', 'IST', 'ZRH', 'VIE']
europe_cities = ['MAN', 'EDI', 'DUB', 'ORY', 'NCE', 'BRU', 'BER', 'GVA', 'MXP', 'VCE', 'BCN', 'AGP', 'LIS', 'OPO', 'CPH', 'ARN', 'OSL', 'HEL', 'WAW', 'PRG', 'BUD', 'OTP', 'SOF', 'BEG']
usa_hubs = ['JFK', 'EWR', 'ORD', 'ATL', 'LAX', 'SFO', 'DFW', 'MIA']
usa_cities = ['BOS', 'IAD', 'PHL', 'MCO', 'DTW', 'MSP', 'SEA', 'LAS', 'PHX', 'DEN', 'IAH']
asia_hubs = ['DXB', 'DOH', 'SIN', 'BKK', 'HKG', 'HND', 'ICN', 'PEK', 'PVG']
australia = ['SYD', 'MEL', 'AKL']



airlines = {
    1: {'name': 'Aegean', 'code': 'A3'},
    2: {'name': 'Sky Express', 'code': 'GQ'},
    3: {'name': 'United', 'code': 'UA'},
    4: {'name': 'Ryanair', 'code': 'FR'},
    5: {'name': 'Emirates', 'code': 'EK'},
    6: {'name': 'Delta', 'code': 'DL'},
    7: {'name': 'Air France', 'code': 'AF'},
    8: {'name': 'Lufthansa', 'code': 'LH'},
    9: {'name': 'British Airways', 'code': 'BA'},
    10: {'name': 'Qatar', 'code': 'QR'},
}



generated_flights = []
flight_counter = 1000

for _ in range(total_flights):
    
   
    scenario = random.choices(
        ['GR_INTERNAL', 'EU_INTERNAL', 'GR_EU', 'US_INTERNAL', 'LONG_HAUL'], 
        weights=[30, 25, 20, 15, 10], 
        k=1
    )[0]

    origin, dest, airline_id, plane_id, duration = "", "", 0, 0, 0

    if scenario == 'GR_INTERNAL':
        # Ελλάδα: Hub <-> Island
        origin = random.choice(greece_hub)
        dest = random.choice(greece_islands)
        if random.random() > 0.5: origin, dest = dest, origin 
        
        airline_id = random.choice([1, 2]) 
        plane_id = random.choice([1, 2, 3]) 
        duration = random.randint(35, 60)
        base_price = random.randint(40, 100)

    elif scenario == 'EU_INTERNAL':
       
        origin = random.choice(europe_hubs)
        dest = random.choice(europe_cities)
        if random.random() > 0.5: origin, dest = dest, origin
        
        airline_id = random.choice([4, 7, 8, 9]) 
        plane_id = random.choice([3, 4, 5]) 
        duration = random.randint(90, 180)
        base_price = random.randint(60, 200)

    elif scenario == 'GR_EU':
        # Ελλάδα <-> Ευρώπη
        origin = random.choice(greece_hub)
        dest = random.choice(europe_hubs)
        if random.random() > 0.5: origin, dest = dest, origin
        
        airline_id = random.choice([1, 4, 8, 9]) 
        plane_id = random.choice([3, 4, 5])
        duration = random.randint(150, 240)
        base_price = random.randint(100, 300)

    elif scenario == 'US_INTERNAL':
        # ΗΠΑ εσωτερικό
        origin = random.choice(usa_hubs)
        dest = random.choice(usa_cities)
        if random.random() > 0.5: origin, dest = dest, origin
        
        airline_id = random.choice([3, 6]) # United, Delta
        plane_id = random.choice([5, 4]) # B737, A321
        duration = random.randint(120, 300)
        base_price = random.randint(150, 450)

    elif scenario == 'LONG_HAUL':
        # Υπερατλαντικά / Ασία (Connecting logic)
        # Από Ευρώπη/ΗΠΑ/Ασία Hub σε άλλο Hub
        hubs = europe_hubs + usa_hubs + asia_hubs + australia
        origin = random.choice(hubs)
        dest = random.choice(hubs)
        while origin == dest: dest = random.choice(hubs) # Σιγουριά ότι δεν είναι ίδιο
        
        airline_id = random.choice([5, 6, 8, 9, 10]) # Emirates, Delta, LH, BA, Qatar
        plane_id = random.choice([6, 7, 8, 9, 10]) # Dreamliner, A350, B777, Jumbo, A380
        duration = random.randint(400, 900)
        base_price = random.randint(500, 1600)

    # --- ΒΗΜΑ Β: ΗΜΕΡΟΜΗΝΙΑ & ΤΙΜΗ ---
    rand_day = random.randint(0, total_days)
    rand_sec = random.randint(0, 86400)
    dep_dt = start_date + timedelta(days=rand_day, seconds=rand_sec)
    arr_dt = dep_dt + timedelta(minutes=duration)

    if dep_dt.month in [6, 7, 8]:
        base_price = base_price * 1.4
    
    final_price = round(base_price, 2)

    # Strings
    dep_str = dep_dt.strftime('%Y-%m-%d %H:%M')
    arr_str = arr_dt.strftime('%Y-%m-%d %H:%M')
    gate = f"{random.choice(['A','B','C','D'])}{random.randint(1,40)}"

    # Κωδικός Πτήσης: παίρνουμε τον IATA κωδικό από το λεξικό `airlines`
    code = airlines.get(airline_id, {}).get('code', 'FL')
    # Δημιουργούμε συνεπή αριθμό πτήσης χωρίς κενό και με padding (π.χ. A31000)
    flight_num = f"{code}{flight_counter:04d}"
    flight_counter += 1

    # SQL Creation
    # Χρησιμοποιούμε subqueries για να βρει το ID βάσει του κωδικού (π.χ. 'JFK')
    sql = (
        f"INSERT INTO pthsh (arithmos_pthshs, etairia_id, aeroplano_id, "
        f"aerodromio_anaxwrhshs_id, aerodromio_afikshs_id, wra_anaxwrhshs, wra_afikshs, pulh, vasikh_timh) "
        f"VALUES ('{flight_num}', {airline_id}, {plane_id}, "
        f"(SELECT aerodromio_id FROM aerodromio WHERE kwdikos='{origin}'), "
        f"(SELECT aerodromio_id FROM aerodromio WHERE kwdikos='{dest}'), "
        f"'{dep_str}', '{arr_str}', '{gate}', {final_price});"
    )
    
    generated_flights.append((dep_dt, sql))

# Ταξινόμηση και Εγγραφή
generated_flights.sort(key=lambda x: x[0])

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"-- ΑΥΤΟΜΑΤΗ ΔΗΜΙΟΥΡΓΙΑ {total_flights} ΠΤΗΣΕΩΝ ΜΕ 150 ΑΕΡΟΔΡΟΜΙΑ\n")
    f.write("-- Καλύπτει περιόδους 2024-2027\n\n")
    for _, sql in generated_flights:
        f.write(sql + "\n")
   

print("DONE")