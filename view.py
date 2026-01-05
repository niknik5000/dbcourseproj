

def print_separator():
    """Τυπώνει μια διαχωριστική γραμμή."""
    print("-" * 60)

def show_header(title, subtitle=None):
    """Εμφανίζει τον τίτλο της οθόνης/μενού."""
    print("\n")
    print("=" * 60)
    print(f"   {title.upper()}")
    if subtitle:
        print(f"   {subtitle}")
    print("=" * 60)

def show_message(message):
    """Εμφανίζει απλό μήνυμα ενημέρωσης."""
    print(f"\n[!] {message}")

def show_error(error_message):
    """Εμφανίζει μήνυμα λάθους."""
    print(f"\n[ERROR] {error_message}")


def show_direct_flights(flights):
    """Εμφανίζει λίστα με απευθείας πτήσεις σε μορφή πίνακα."""
    if not flights:
        print("\n   Δεν βρέθηκαν απευθείας πτήσεις.")
        return

    print("\nΑΠΕΥΘΕΙΑΣ ΠΤΗΣΕΙΣ:")
    print_separator()
    print(f"{'ΚΩΔΙΚΟΣ':<10} {'ΕΤΑΙΡΙΑ':<15} {'ΑΝΑΧΩΡΗΣΗ':<18} {'ΤΙΜΗ'}")
    print_separator()

    for f in flights:
        code = f['arithmos_pthshs']
        airline = f['etairia'][:14] 
        dep_time = f['wra_anaxwrhshs']
        price = f"{f['vasikh_timh']} EUR"
        
        print(f"{code:<10} {airline:<15} {dep_time:<18} {price}")
    print_separator()

def show_connecting_flights(flights, stops=1):
    """Εμφανίζει πτήσεις με ανταπόκριση."""
    if not flights:
        return 

    title = "ΠΤΗΣΕΙΣ ΜΕ 1 ΣΤΑΣΗ" if stops == 1 else "ΠΤΗΣΕΙΣ ΜΕ 2 ΣΤΑΣΕΙΣ"
    print(f"\n{title}:")
    print_separator()

    for i, f in enumerate(flights, 1):
        if stops == 1:
            print(f"{i}. ΜΕ ΑΛΛΑΓΗ ΣΤΟ: {f['via']}")
            print(f"   ΣΚΕΛΟΣ 1: {f['origin']} -> {f['via']} ({f['flight1']})")
            print(f"   ΣΚΕΛΟΣ 2: {f['via']} -> {f['destination']} ({f['flight2']})")
        else:
            # Περίπτωση 2 στάσεων (3 legs)
            print(f"{i}. ΜΕ ΑΛΛΑΓΕΣ ΣΕ: {f['via1']} ΚΑΙ {f['via2']}")
            print(f"   ΣΚΕΛΟΣ 1: {f['origin']} -> {f['via1']} ({f['flight1']})")
            print(f"   ΣΚΕΛΟΣ 2: {f['via1']} -> {f['via2']} ({f['flight2']})")
            print(f"   ΣΚΕΛΟΣ 3: {f['via2']} -> {f['destination']} ({f['flight3']})")
            
        print(f"   ΣΥΝΟΛΟ ΤΙΜΗΣ: {f['total_price']} EUR")
        print("-" * 30)


def show_seats(seats, category_name="Economy"):
    """Εμφανίζει τις διαθέσιμες θέσεις σε απλή διάταξη."""
    print(f"\nΔΙΑΘΕΣΙΜΕΣ ΘΕΣΕΙΣ ({category_name}):")
    print(f"Σύνολο: {len(seats)}")
    print("-" * 40)
    
    
    row_str = ""
    for i, seat in enumerate(seats):
        row_str += f"[{seat}]  "
        if (i + 1) % 6 == 0:
            print(row_str)
            row_str = ""
    
    if row_str:
        print(row_str)
    print("-" * 40)


def show_booking_history(bookings):
    """Εμφανίζει το ιστορικό κρατήσεων."""
    if not bookings:
        print("\nΔεν βρέθηκαν κρατήσεις.")
        return

    print("\nΙΣΤΟΡΙΚΟ ΚΡΑΤΗΣΕΩΝ:")
    print_separator()
    for b in bookings:
        print(f"ID: {b['ar_krathshs']} | ΗΜ/ΝΙΑ: {b['hmeromhnia_krathshs']}")
        print(f"   ΠΤΗΣΗ: {b['arithmos_pthshs']} ({b['apo']} -> {b['pros']})")
        print(f"   ΑΤΟΜΑ: {b['ar_atomwn']} | ΚΟΣΤΟΣ: {b['sunoliko_kostos']} EUR")
        print("-" * 30)

def show_passenger_list(passengers):
    """Λίστα επιβατών (Admin)."""
    if not passengers:
        print("Κανένας επιβάτης.")
        return
        
    print(f"\n{'ΟΝΟΜΑ':<15} {'ΕΠΙΘΕΤΟ':<15} {'ΔΙΑΒΑΤΗΡΙΟ':<12} {'ΘΕΣΗ'}")
    print("-" * 55)
    for p in passengers:
        print(f"{p['onoma']:<15} {p['epitheto']:<15} {p['at_diabathrio']:<12} {p['arithmos_theshs']}")