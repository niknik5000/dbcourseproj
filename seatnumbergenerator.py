
from pathlib import Path

# set output path to script folder
script_dir = Path(__file__).resolve().parent
filename = script_dir / "seats.txt"

print(f"creating file {filename}...")

with open(filename, "w", encoding="utf-8") as f:

    f.write("-- ΜΙΚΡΑ ΑΕΡΟΠΛΑΝΑ (100 Θέσεις - Economy)\n")
    small_planes = [1, 2] 
    # loop each plane and generate rows 1-25, columns a-d
    for plane_id in small_planes:
        for row in range(1, 26): 
            for seat in "ABCD":
                sql = f"INSERT INTO thesh (aeroplano_id, katigoria_id, arithmos_theshs) VALUES ({plane_id}, 1, '{row}{seat}');\n"
                f.write(sql)
    
    f.write("\n")

    f.write("-- ΜΕΣΑΙΑ ΑΕΡΟΠΛΑΝΑ (~250 Θέσεις - Business/Economy)\n")
    medium_planes = [3, 4, 5]

    # rows 1-5 are business, rest are economy
    for plane_id in medium_planes:
        for row in range(1, 43): 
            for seat in "ABCDEF":
                if row <= 5:
                    cat_id = 2 
                else:
                    cat_id = 1
                
                sql = f"INSERT INTO thesh (aeroplano_id, katigoria_id, arithmos_theshs) VALUES ({plane_id}, {cat_id}, '{row}{seat}');\n"
                f.write(sql)

    f.write("\n")

    f.write("-- ΜΕΓΑΛΑ ΑΕΡΟΠΛΑΝΑ (400 Θέσεις - First/Business/Economy)\n")
    large_planes = [6, 7, 8, 9, 10]

    # rows 1-4 first class, 5-12 business, rest economy
    for plane_id in large_planes:
        for row in range(1, 51): 
            for seat in "ABCDEFGH":
                if row <= 4:
                    cat_id = 3 
                elif row <= 12:
                    cat_id = 2 
                else:
                    cat_id = 1 
                
                sql = f"INSERT INTO thesh (aeroplano_id, katigoria_id, arithmos_theshs) VALUES ({plane_id}, {cat_id}, '{row}{seat}');\n"
                f.write(sql)




print("done")