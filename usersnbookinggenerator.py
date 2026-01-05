import random
from datetime import datetime, timedelta
from pathlib import Path

# set output path to script folder
script_dir = Path(__file__).resolve().parent
filename = script_dir / "NEWbookings.txt"

# data sizes
num_users = 80           
num_bookings = 200       
total_flights_est = 3000 

# name pools for random selection
first_names = [
    "Giorgos", "Dimitris", "Yannis", "Nikos", "Kostas", "Christos", "Panagiotis", 
    "Vasilis", "Thanos", "Alexandros", "Michalis", "Spyros",
    "Maria", "Eleni", "Katerina", "Georgia", "Sofia", "Anna", "Dimitra", 
    "Ioanna", "Vasiliki", "Anastasia", "Christina", "Zoe",
    "John", "David", "Michael", "James", "Robert", "William",
    "Sarah", "Emily", "Bruce", "Jennifer", "Lisa", "Elizabeth"
]

last_names = [
    "Ploumpidis", "Karavasilis", "Oikonomou", "Georgiou", "Karagiannis", "Makris",
    "Papageorgiou", "Dimopoulos", "Kotsis", "Papas", "Stefanou", "Louris", "Nikas",
    "Smith", "Johnson", "Williams", "Wayne", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson"
]

streets = ["Street", "Road", "Avenue", "Boulevard", "Central", "Presidents", "Main St"]
cities = ["BIG city", "Small City", "Capital", "Enemy City", "Gotham"]

# generate random phone number
def get_phone():
    return f"69{random.randint(10000000, 99999999)}"

# generate random password
def get_password():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(8))


with open(filename, "w", encoding="utf-8") as f:

    f.write("-- Α. ΧΡΗΣΤΕΣ\n")
    
   
    
    for i in range(1, num_users + 1):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        
        # generate email from names
        email = f"{fname.lower()}.{lname.lower()}{random.randint(1,999)}@mail.com"
        phone = get_phone()
        password = get_password()
        
        # random address
        city = random.choice(cities)
        addr = f"{random.choice(streets)} {random.randint(1, 150)}, {city}"

        sql = (
            f"INSERT INTO xrhsths (onoma, epitheto, email, thlefwno, dieuthunsh, kwdikos) "
            f"VALUES ('{fname}', '{lname}', '{email}', '{phone}', '{addr}', '{password}');"
        )
        f.write(sql + "\n")


    f.write("\n")

 
    f.write("-- ΕΠΙΒΑΤΕΣ \n")
   
    for i in range(1, 151):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
      # generate document id
        doc_id = f"{random.choice(['AN','AB','X','P'])}{random.randint(100000, 999999)}"
        
        
        sql = f"INSERT INTO epivaths (onoma, epitheto, at_diabathrio) VALUES ('{fname}', '{lname}', '{doc_id}');"
        f.write(sql + "\n")
    f.write("\n")


 
    f.write("-- ΚΡΑΤΗΣΕΙΣ\n")

    for k in range(1, num_bookings + 1):
        # pick random flight
        flight_id = random.randint(1, total_flights_est)
        
  # random booking date in 2024
        b_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 360))
        b_date_str = b_date.strftime('%Y-%m-%d %H:%M:%S')

        # number of passengers per booking
        num_tickets = random.choice([1, 1, 1, 2, 2, 3]) 
        
      # insert booking record
       
        sql_k = (
            f"INSERT INTO krathsh (xrhsths_id, hmeromhnia_krathshs, sunoliko_kostos, ar_atomwn) "
            f"VALUES ("
            f"(SELECT xrhsths_id FROM xrhsths ORDER BY RANDOM() LIMIT 1), "
            f"'{b_date_str}', "
            f"(SELECT vasikh_timh * {num_tickets} FROM pthsh WHERE pthsh_id = {flight_id}), "
            f"{num_tickets});"
        )
        f.write(sql_k + "\n")
      # insert ticket for each passenger
        for _ in range(num_tickets):
            sql_t = (
                f"INSERT INTO eisithrio (krathsh_id, pthsh_id, epivaths_id, arithmos_theshs, timh, hmeromhnia_wra) "
                f"SELECT last_insert_rowid(), {flight_id}, e.epivaths_id, t.arithmos_theshs, "
                f"(SELECT vasikh_timh FROM pthsh WHERE pthsh_id = {flight_id}), "
                f"'{b_date_str}' "
                f"FROM thesh t "
                f"JOIN pthsh p ON t.aeroplano_id = p.aeroplano_id "
                f"CROSS JOIN (SELECT epivaths_id FROM epivaths ORDER BY RANDOM() LIMIT 1) e "
                f"WHERE p.pthsh_id = {flight_id} "
                f"AND t.arithmos_theshs NOT IN (SELECT arithmos_theshs FROM eisithrio WHERE pthsh_id = {flight_id}) "
                f"ORDER BY RANDOM() LIMIT 1;"
            )
            f.write(sql_t + "\n")

print("DONE")