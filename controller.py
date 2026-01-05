import sys
from model import (
    find_email, register_user,
    search_direct_flights, search_connecting_flights, search_3_leg_flights,
    get_flight_id, get_available_seats, create_booking_transaction,
    get_user_bookings, cancel_booking,
    admin_get_passengers, admin_add_flight, admin_get_all_flights,
)
from view import (
    show_header, show_message, show_error,
    show_direct_flights, show_connecting_flights, show_seats,
    show_booking_history, show_passenger_list
)


current_user = None


def do_search():
    """Διαδικασία Αναζήτησης."""
    print("\n--- ΑΝΑΖΗΤΗΣΗ ---")
    origin = input("Από (Πόλη): ")
    dest = input("Προς (Πόλη): ")
    found_something = False
    selected_flights = []
    
    print(f"\nΨάχνω απευθείας πτήσεις από {origin} προς {dest}...")
    direct = search_direct_flights(origin, dest)
    if direct:
        show_direct_flights(direct)
        found_something = True
        selected_flights = direct
        print("\n(-> Βρέθηκαν απευθείας πτήσεις.)")
    
    if not found_something:
        print("-> Δεν βρέθηκαν απευθείας πτήσεις. Ψάχνω με 1 ανταπόκριση...")
        conn1 = search_connecting_flights(origin, dest)
        
        if conn1:
            show_connecting_flights(conn1, stops=1)
            found_something = True
            selected_flights = conn1
            print("\n(-> Βρέθηκαν πτήσεις με 1 ανταπόκριση.)")
    
    if not found_something:
        print("-> Δεν βρέθηκαν ούτε πτήσεις με 1 ανταπόκριση. Ψάχνω με 2 ανταποκρίσεις...")
        conn2 = search_3_leg_flights(origin, dest)
        
        if conn2:
            show_connecting_flights(conn2, stops=2)
            found_something = True
            selected_flights = conn2

    if not found_something:
        print(f"\n[X] Δυστυχώς, ΔΕΝ βρέθηκαν πτήσεις από '{origin}' προς '{dest}'.")
        print("Δοκιμάστε άλλες ημερομηνίες ή αεροδρόμια.")
        return
    
    book_choice = input("\nΘέλετε να κάνετε κράτηση από αυτές τις πτήσεις; (y/n): ").lower()
    if book_choice == 'y':
        flight_code = input("Δώστε τον κωδικό πτήσης που θέλετε: ").strip()
        proceed_with_booking(flight_code)
    else:
        None

def proceed_with_booking(flight_code):
    """Διαδικασία Κράτησης για συγκεκριμένη πτήση."""
    try:
        flight_info = get_flight_id(flight_code)
        if not flight_info:
            show_error("Η πτήση δεν βρέθηκε.")
            return
        base_price = flight_info['vasikh_timh']
        economy_price = base_price
        business_price = base_price * 1.5
        first_price = base_price * 2.0
        
        print("\nΕπιλογή Κατηγορίας:")
        print(f"1. Economy      {economy_price} EUR")
        print(f"2. Business     {business_price} EUR (+50%)")
        print(f"3. First Class  {first_price} EUR (+100%)")

        
        cat_in = input("Επιλογή (1-3) [Default: 1]: ").strip()
        
        if cat_in == '2':
            seat_type = "Business"
            multiplier = 1.5
            selected_price = business_price
        elif cat_in == '3':
            seat_type = "First Class"
            multiplier = 2.0
            selected_price = first_price
        else:
            seat_type = "Economy"
            multiplier = 1.0
            selected_price = economy_price
        
        print(f"\n Επιλεγμένη κατηγορία: {seat_type} ({selected_price} EUR ανά άτομο)")



        print(f"\nΈλεγχος για {seat_type}...")
        seats = get_available_seats(flight_code, seat_type)
        
        if not seats:
            if seat_type == "First Class":
                print(f"[!] Δεν υπάρχουν θέσεις First Class.")
                print("-> Ψάχνω για Business seats")
                seats = get_available_seats(flight_code, "Business")
                
                if seats:
                    fallback = input("Διαθέσιμες θέσεις Business. Θέλετε Business με +50%; (y/n): ").lower()
                    if fallback == 'y':
                        seat_type = "Business"
                        multiplier = 1.5
                    else:
                        return
                else:
                    print("-> Δεν υπάρχουν Business seats. Ψάχνω για Economy...")
                    seats = get_available_seats(flight_code, "Economy")
                    if seats:
                        seat_type = "Economy"
                        multiplier = 1.0
                    else:
                        show_error("Η πτήση είναι ΓΕΜΑΤΗ.")
                        return
            
            elif seat_type == "Business":
                print(f"[!] Δεν υπάρχουν θέσεις Business.")
                print("-> Ψάχνω για Economy seats...")
                seats = get_available_seats(flight_code, "Economy")
                
                if seats:
                    fallback = input("Διαθέσιμες θέσεις Economy. Θέλετε Economy με βασική τιμή; (y/n): ").lower()
                    if fallback == 'y':
                        seat_type = "Economy"
                        multiplier = 1.0
                    else:
                        return
                else:
                    show_error("Η πτήση είναι ΓΕΜΑΤΗ.")
                    return
            else:
                show_error("Η πτήση είναι ΓΕΜΑΤΗ.")
                return
        
        show_seats(seats, seat_type)

        try:
            num_pax = int(input("\nΑριθμός Επιβατών: "))
            if num_pax > len(seats):
                show_error("Δεν υπάρχουν αρκετές θέσεις.")
                return
        except ValueError:
            show_error("Λάθος αριθμός.")
            return

        passengers = []
        final_price = flight_info['vasikh_timh'] * multiplier
        print(f"\nΤΙΜΗ ΑΝΑ ΑΤΟΜΟ: {final_price} EUR ({seat_type})")

        for i in range(num_pax):
            print(f"\n--- Επιβάτης {i+1} ---")
            fname = input("Όνομα: ")
            lname = input("Επίθετο: ")
            passp = input("Αρ. Ταυτότητας/Διαβατηρίου: ")
            
            while True:
                s_choice = input("Επιλογή Θέσης (από τις διαθέσιμες): ").strip()
                current_selection = [p['seat'] for p in passengers]
                
                if s_choice in seats and s_choice not in current_selection:
                    passengers.append({'fname': fname, 'lname': lname, 'passport': passp, 'seat': s_choice})
                    break
                else:
                    print("Λάθος επιλογή θέσης (κατειλημμένη ή μη-υπάρχουσα).")


        total = final_price * num_pax
        print(f"\nΣΥΝΟΛΙΚΟ ΚΟΣΤΟΣ: {total} EUR")
        confirm = input("Προχωράμε σε κράτηση; (y/n): ").lower()
        
        if confirm == 'y':
            bid = create_booking_transaction(current_user['xrhsths_id'], flight_info['pthsh_id'], final_price, passengers)
            if bid:
                show_message(f"Η Κράτηση #{bid} έγινε επιτυχώς!")
            else:
                show_error("Η κράτηση απέτυχε.")
        else:
            print("Ακύρωση.")

    except Exception as e:
        show_error(f"Σφάλμα συστήματος: {e}")

def do_history():
    """Ιστορικό και Ακύρωση."""
    bookings = get_user_bookings(current_user['xrhsths_id'])
    show_booking_history(bookings)
    
    if bookings:
        print("\nΓια ακύρωση, γράψτε το ID της κράτησης (αλλιώς Enter για επιστροφή).")
        cancel_id = input("ID: ").strip()
        if cancel_id:
            try:
                bid = int(cancel_id)
                if cancel_booking(bid, current_user['xrhsths_id']):
                    show_message("Η κράτηση ακυρώθηκε.")
                else:
                    show_error("Η ακύρωση απέτυχε.")
            except ValueError:
                pass




def handle_login():
    global current_user
    show_header("ΕΙΣΟΔΟΣ ΧΡΗΣΤΗ")
    
    email = input("E-mail: ").strip()
    
    if email == "admin":
        admin_pwd = input("Κωδικός: ").strip()
        if admin_pwd == "admin":
            current_user = {'xrhsths_id': 0, 'onoma': 'Admin', 'epitheto': 'System', 'role': 'admin'}
            return
        else:
            show_error("Λάθος κωδικός!")
            return

    user = find_email(email)
    
    if user:
        password = input("Κωδικός: ").strip()
        if password == user['kwdikos']:
            current_user = user
            current_user['role'] = 'customer'
            show_message(f"Καλώς ήρθατε, {user['onoma']}!")
        else:
            show_error("Λάθος κωδικός!")
    else:
        print("\nΔεν βρέθηκε λογαριασμός.")
        choice = input("Θέλετε να κάνετε εγγραφή; (y/n): ").lower()
        
        if choice == 'y':
            print("\nΦΟΡΜΑ ΕΓΓΡΑΦΗΣ")
            fname = input("Όνομα: ")
            lname = input("Επίθετο: ")
            phone = input("Τηλέφωνο: ")
            addr = input("Διεύθυνση: ")
            password = input("Κωδικός: ")
            
            new_id = register_user(fname, lname, email, phone, addr, password)
            if new_id:
                current_user = {
                    'xrhsths_id': new_id,
                    'onoma': fname,
                    'epitheto': lname,
                    'email': email,
                    'role': 'customer'
                }
                show_message("Η εγγραφή ολοκληρώθηκε!")
            else:
                show_error("Η εγγραφή απέτυχε.")

def customer_menu():
    while True:
        show_header("ΜΕΝΟΥ ΠΕΛΑΤΗ", f"Χρήστης: {current_user['onoma']}")
        print("1. Αναζήτηση Πτήσεων")
        print("2. Ιστορικό & Ακυρώσεις")
        print("0. Έξοδος")
        
        choice = input("\nΕπιλογή: ").strip()
        
        if choice == '1':
            do_search()
        elif choice == '2':
            do_history()
        elif choice == '0':
            print("Αντίο!")
            sys.exit()
        else:
            show_error("Λάθος επιλογή.")

def admin_menu():
    while True:
        show_header("ΜΕΝΟΥ ΔΙΑΧΕΙΡΙΣΤΗ (ADMIN)")
        print("1. Λίστα Επιβατών Πτήσης")
        print("2. Προσθήκη Νέας Πτήσης")
        print("3. Προβολή ΟΛΩΝ των Πτήσεων (Ιστορικό)")
        print("0. Έξοδος")
        
        choice = input("\nΕπιλογή: ").strip()
        
        if choice == '1':
            code = input("Δώστε Κωδικό Πτήσης: ").strip()
            flight = get_flight_id(code)
            if not flight:
                show_error("Η πτήση δεν βρέθηκε.")
                continue
            pax = admin_get_passengers(code)
            show_passenger_list(pax)

        elif choice == '2':
            try:
                print("\nΠΡΟΣΘΗΚΗ ΠΤΗΣΗΣ")
                code = input("Κωδικός Πτήσης: ")
                airline_name = input("Όνομα Εταιρίας: ")
                plane_model = input("Μοντέλο Αεροπλάνου: ")
                dep_iata = input("IATA Κωδικός Αναχώρησης (π.χ. ATH): ").strip().upper()
                arr_iata = input("IATA Κωδικός Άφιξης (π.χ. AMS): ").strip().upper()
                time_dep = input("Ώρα Αναχώρησης (YYYY-MM-DD HH:MM): ")
                time_arr = input("Ώρα Άφιξης (YYYY-MM-DD HH:MM): ")
                gate = input("Πύλη (Gate): ")
                price = float(input("Βασική Τιμή: "))
                
                res = admin_add_flight(code, airline_name, plane_model, dep_iata, arr_iata, time_dep, time_arr, gate, price)
                if res: show_message("Η πτήση προστέθηκε!")
                else: show_error("Αποτυχία.")
            except ValueError:
                show_error("Λάθος μορφή δεδομένων.")

        elif choice == '3':
            all_flights = admin_get_all_flights()
            if all_flights:
                print("\nΟΛΕΣ ΟΙ ΠΤΗΣΕΙΣ:")
                print(f"{'ΚΩΔΙΚΟΣ':<10} {'ΑΠΟ':<15} {'ΠΡΟΣ':<15} {'ΗΜΕΡΟΜΗΝΙΑ'}")
                print("-" * 60)
                for f in all_flights:
                    print(f"{f['arithmos_pthshs']:<10} {f['apo']:<15} {f['pros']:<15} {f['wra_anaxwrhshs']}")
                print("-" * 60)
            else:
                print("Δεν υπάρχουν πτήσεις στη βάση.")

        elif choice == '0':
            sys.exit()

def main():
    while True:
        if not current_user:
            handle_login()
        else:
            if current_user.get('role') == 'admin':
                admin_menu()
            else:
                customer_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nΈξοδος")