import sqlite3

DB_NAME = "NEWflightmanagement.db"

#connect to the database
def get_connection():
    try:
        con = sqlite3.connect(DB_NAME)
        con.execute("PRAGMA foreign_keys = ON;")
        con.row_factory = sqlite3.Row 
        return con
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    

#check if user exists by email
def find_email(email):
    sql = "SELECT * FROM xrhsths WHERE email = ?"
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    except sqlite3.Error as e:
        print(f"Login error: {e}")
        return None
    

#register a new user
def register_user(first_name, last_name, email, phone, address, kwdikos):
    sql = """
    INSERT INTO xrhsths (onoma, epitheto, email, thlefwno, dieuthunsh, kwdikos)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (first_name, last_name, email, phone, address, kwdikos))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Registration error: {e}")
        return None
    

#search direct flights
def search_direct_flights(origin, destination):
    sql = """
    SELECT 
        p.arithmos_pthshs,
        e.onoma AS etairia,
        a1.polh AS apo_polh,
        a2.polh AS pros_polh,
        p.wra_anaxwrhshs,
        p.vasikh_timh
    FROM pthsh p
    JOIN etairia e ON p.etairia_id = e.etairia_id
    JOIN aerodromio a1 ON p.aerodromio_anaxwrhshs_id = a1.aerodromio_id
    JOIN aerodromio a2 ON p.aerodromio_afikshs_id = a2.aerodromio_id
    WHERE a1.polh LIKE ? AND a2.polh LIKE ?
    AND p.wra_anaxwrhshs > datetime('now')
    ORDER BY p.wra_anaxwrhshs;
    """
    results = []
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (f"%{origin}%", f"%{destination}%"))
            for row in cursor.fetchall():
                results.append(dict(row))
        return results
    except sqlite3.Error as e:
        print(f"Search error: {e}")
        return []
    

#search connecting flights 1 stop
def search_connecting_flights(origin, destination):
    sql = """
    SELECT 
        p1.arithmos_pthshs AS flight1,
        dep.polh AS origin,
        hub.polh AS via,
        p2.arithmos_pthshs AS flight2,
        arr.polh AS destination,
        (p1.vasikh_timh + p2.vasikh_timh) AS total_price,
        p1.wra_anaxwrhshs AS departure_time
    FROM pthsh p1
    JOIN pthsh p2 ON p1.aerodromio_afikshs_id = p2.aerodromio_anaxwrhshs_id
    JOIN aerodromio dep ON p1.aerodromio_anaxwrhshs_id = dep.aerodromio_id
    JOIN aerodromio hub ON p1.aerodromio_afikshs_id = hub.aerodromio_id
    JOIN aerodromio arr ON p2.aerodromio_afikshs_id = arr.aerodromio_id
    WHERE dep.polh LIKE ? 
      AND arr.polh LIKE ?
      AND p2.wra_anaxwrhshs > p1.wra_afikshs
      AND (julianday(p2.wra_anaxwrhshs) - julianday(p1.wra_afikshs)) < 1
      AND p1.wra_anaxwrhshs > datetime('now')
    ORDER BY total_price ASC LIMIT 5;
    """
 
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (f"%{origin}%", f"%{destination}%"))
            colnames = [d[0] for d in cursor.description]
            return [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except sqlite3.Error:
        print("Error in connecting flights search")
        return []
    
#search connecting flights 2 stops
def search_3_leg_flights(origin, destination):
    sql = """
    SELECT 
        -- flight 1
        p1.arithmos_pthshs AS flight1,
        dep.polh AS origin,
        hub1.polh AS via1,
        
        -- flight 2
        p2.arithmos_pthshs AS flight2,
        hub2.polh AS via2,
        
        -- flight 3
        p3.arithmos_pthshs AS flight3,
        arr.polh AS destination,
        
        -- total
        (p1.vasikh_timh + p2.vasikh_timh + p3.vasikh_timh) AS total_price
        
    FROM pthsh p1
    JOIN pthsh p2 ON p1.aerodromio_afikshs_id = p2.aerodromio_anaxwrhshs_id
    JOIN pthsh p3 ON p2.aerodromio_afikshs_id = p3.aerodromio_anaxwrhshs_id
    JOIN aerodromio dep ON p1.aerodromio_anaxwrhshs_id = dep.aerodromio_id
    JOIN aerodromio hub1 ON p1.aerodromio_afikshs_id = hub1.aerodromio_id
    JOIN aerodromio hub2 ON p2.aerodromio_afikshs_id = hub2.aerodromio_id
    JOIN aerodromio arr ON p3.aerodromio_afikshs_id = arr.aerodromio_id
    
    WHERE dep.polh LIKE ?     
      AND arr.polh LIKE ?       
      
      -- Time constraints (next flight departs after previous flight arrives)
      AND p2.wra_anaxwrhshs > p1.wra_afikshs
      AND (julianday(p2.wra_anaxwrhshs) - julianday(p1.wra_afikshs)) < 1
      AND p3.wra_anaxwrhshs > p2.wra_afikshs
      AND (julianday(p3.wra_anaxwrhshs) - julianday(p2.wra_afikshs)) < 1
      AND p1.wra_anaxwrhshs > datetime('now')
      
    ORDER BY total_price ASC LIMIT 3;
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (f"%{origin}%", f"%{destination}%"))
            colnames = [d[0] for d in cursor.description]
            return [dict(zip(colnames, row)) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error in 3-leg flights: {e}")
        return []
    


#helper to get flight id by flight code
def get_flight_id(flight_code):
 
    sql = "SELECT pthsh_id, vasikh_timh FROM pthsh WHERE arithmos_pthshs = ?"
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (flight_code,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error:
        return None


#gets list of available seats
def get_available_seats(flight_code, seat_type=None):
 
    sql1 = """
    SELECT t.arithmos_theshs
    FROM thesh t
    JOIN pthsh p ON t.aeroplano_id = p.aeroplano_id
    JOIN katigoria_theshs k ON t.katigoria_id = k.katigoria_id
    WHERE p.arithmos_pthshs = ?
    """
    params = [flight_code]
    if seat_type:
        sql1 += " AND k.onoma = ?"
        params.append(seat_type)

    sql2 = """
    EXCEPT
    SELECT e.arithmos_theshs
    FROM eisithrio e
    JOIN pthsh p ON e.pthsh_id = p.pthsh_id
    WHERE p.arithmos_pthshs = ?
    ORDER BY t.arithmos_theshs;
    """
    params.append(flight_code)

    sql = sql1 + sql2
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, tuple(params))
            return [row['arithmos_theshs'] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"seats error: {e}")
        return []



# booking transaction
# passenger_list = [{'fname': 'John', 'lname': 'Doe', 'passport': 'A1234567', 'seat': '12A'}, ...]
def create_booking_transaction(user_id, flight_id, price, passenger_list):

    con = get_connection()
    if not con: return None
    
    try:
        cursor = con.cursor()
        
        # creating a booking
        total_cost = price * len(passenger_list)
        cursor.execute("""
            INSERT INTO krathsh (xrhsths_id, hmeromhnia_krathshs, sunoliko_kostos, ar_atomwn)
            VALUES (?, datetime('now'), ?, ?)
        """, (user_id, total_cost, len(passenger_list)))
        
        booking_id = cursor.lastrowid #get id
        
        for p in passenger_list:
            
            cursor.execute("""
                INSERT INTO epivaths (onoma, epitheto, at_diabathrio) 
                VALUES (?, ?, ?)
            """, (p['fname'], p['lname'], p['passport']))
            
            passenger_id = cursor.lastrowid #get id
            
            
            cursor.execute("""
                INSERT INTO eisithrio (krathsh_id, pthsh_id, epivaths_id, arithmos_theshs, timh, hmeromhnia_wra)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (booking_id, flight_id, passenger_id, p['seat'], price))
        
        
        con.commit()
        print(" Η συναλλαγή ολοκληρώθηκε επιτυχώς!")
        return booking_id

    except sqlite3.Error as e:

        con.rollback()
        print(f" Booking error (Rollback): {e}")
        return None
    finally:
        con.close()


def get_user_bookings(user_id):
    sql = """
    SELECT 
        k.ar_krathshs, 
        k.hmeromhnia_krathshs, 
        k.sunoliko_kostos, 
        k.ar_atomwn,
        p.arithmos_pthshs,
        dep.polh AS apo,
        arr.polh AS pros
    FROM krathsh k
    JOIN eisithrio e ON k.ar_krathshs = e.krathsh_id
    JOIN pthsh p ON e.pthsh_id = p.pthsh_id
    JOIN aerodromio dep ON p.aerodromio_anaxwrhshs_id = dep.aerodromio_id
    JOIN aerodromio arr ON p.aerodromio_afikshs_id = arr.aerodromio_id
    WHERE k.xrhsths_id = ?
    GROUP BY k.ar_krathshs
    ORDER BY k.hmeromhnia_krathshs DESC;
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"booking history error: {e}")
        return []

def cancel_booking(booking_id, user_id):
    con = get_connection()
    if not con: return False
    
    try:
        cursor = con.cursor()
        
        cursor.execute("""
            SELECT epivaths_id FROM eisithrio WHERE krathsh_id = ?
        """, (booking_id,))
        passenger_ids = [row['epivaths_id'] for row in cursor.fetchall()]
        
        cursor.execute("DELETE FROM eisithrio WHERE krathsh_id = ?", (booking_id,))
        
        for pid in passenger_ids:
            cursor.execute("""
                DELETE FROM epivaths WHERE epivaths_id = ? 
                AND epivaths_id NOT IN (SELECT epivaths_id FROM eisithrio)
            """, (pid,))
        
        cursor.execute("""
            DELETE FROM krathsh WHERE ar_krathshs = ? AND xrhsths_id = ?
        """, (booking_id, user_id))
        
        con.commit()
        
        if cursor.rowcount > 0:
            return True 
        else:
            return False #booking not found
    except sqlite3.Error as e:
        con.rollback()
        print(f"cancel error: {e}")
        return False
    finally:
        con.close()
    

#admin functions 
def admin_get_passengers(flight_code):

    sql = """
    SELECT 
        ep.onoma, 
        ep.epitheto, 
        ep.at_diabathrio, 
        e.arithmos_theshs
    FROM eisithrio e
    JOIN epivaths ep ON e.epivaths_id = ep.epivaths_id
    JOIN pthsh p ON e.pthsh_id = p.pthsh_id
    WHERE p.arithmos_pthshs = ?
    ORDER BY e.arithmos_theshs;
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (flight_code,))
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Admin Error: {e}")
        return []


def get_airline_id_by_name(airline_name):
    sql = "SELECT etairia_id FROM etairia WHERE onoma LIKE ?"
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (f"%{airline_name}%",))
            row = cursor.fetchone()
            return row['etairia_id'] if row else None
    except sqlite3.Error:
        return None

def get_plane_id_by_model(plane_model):
    sql = "SELECT aeroplano_id FROM aeroplano WHERE montelo LIKE ?"
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (f"%{plane_model}%",))
            row = cursor.fetchone()
            return row['aeroplano_id'] if row else None
    except sqlite3.Error:
        return None


def get_airport_id_by_iata(iata_code):
    sql = "SELECT aerodromio_id FROM aerodromio WHERE kwdikos = ?"
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (iata_code.upper(),))
            row = cursor.fetchone()
            return row['aerodromio_id'] if row else None
    except sqlite3.Error:
        return None


def admin_add_flight(flight_code, airline_name, plane_model, from_iata, to_iata, dept_time, arr_time, gate, price):
    """Add a new flight using airline name, plane model, and airport IATA codes."""

    airline_id = get_airline_id_by_name(airline_name)
    if not airline_id:
        print(f"Σφάλμα: Η εταιρία '{airline_name}' δεν βρέθηκε.")
        return None
    
    plane_id = get_plane_id_by_model(plane_model)
    if not plane_id:
        print(f"Σφάλμα: Το αεροπλάνο '{plane_model}' δεν βρέθηκε.")
        return None
    
    from_id = get_airport_id_by_iata(from_iata)
    if not from_id:
        print(f"Σφάλμα: Το αεροδρόμιο '{from_iata}' δεν βρέθηκε.")
        return None
    
    to_id = get_airport_id_by_iata(to_iata)
    if not to_id:
        print(f"Σφάλμα: Το αεροδρόμιο '{to_iata}' δεν βρέθηκε.")
        return None
    
    sql = """
    INSERT INTO pthsh (arithmos_pthshs, etairia_id, aeroplano_id, 
                       aerodromio_anaxwrhshs_id, aerodromio_afikshs_id, 
                       wra_anaxwrhshs, wra_afikshs, pulh, vasikh_timh)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, (flight_code, airline_id, plane_id, from_id, to_id, dept_time, arr_time, gate, price))
            con.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Add Flight Error: {e}")
        return None


def get_all_airports():
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute("SELECT aerodromio_id, kwdikos, polh FROM aerodromio")
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error:
        return []

  
def admin_get_all_flights():

    sql = """
    SELECT 
        p.arithmos_pthshs,
        dep.polh AS apo,
        arr.polh AS pros,
        p.wra_anaxwrhshs,
        p.vasikh_timh
    FROM pthsh p
    JOIN aerodromio dep ON p.aerodromio_anaxwrhshs_id = dep.aerodromio_id
    JOIN aerodromio arr ON p.aerodromio_afikshs_id = arr.aerodromio_id
    ORDER BY p.wra_anaxwrhshs DESC;
    """
    try:
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error:
        return []