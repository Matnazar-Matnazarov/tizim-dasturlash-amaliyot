"""
30.Binar faylni matnli faylga (JSON) aylantiruvchi konvertor yarating.
"""

import struct
import json

def save_students(filename, students):
    with open(filename, 'wb') as f:
        for id, name, grade in students:
            f.write(struct.pack('i20sf', id, name.encode(), grade))

def bin_to_json(bin_file, json_file):
    students = []
    
    with open(bin_file, 'rb') as f:
        while True:
            data = f.read(28)        
            if not data: 
                break
                
            id, name_bytes, grade = struct.unpack('i20sf', data)
            name = name_bytes.decode().rstrip('\x00')
            
            students.append({"id": id, "name": name, "grade": grade})
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=4, ensure_ascii=False)
    
    print("Tayyor! →", json_file)

if __name__ == "__main__":
    talabalar = [
        (1, "Ali", 4.5),
        (2, "Vali", 3.8),
        (3, "Olim", 5.0),
        (4, "Sardor", 4.9)
    ]
    
    save_students("talabalar.bin", talabalar)
    bin_to_json("talabalar.bin", "talabalar.json")