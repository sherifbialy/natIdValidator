from datetime import datetime

GOVERNORATES = {
    "01": "Cairo",
    "02": "Alexandria",
    "03": "Port Said",
    "04": "Suez",
    "11": "Damietta",
    "12": "Dakahlia",
    "13": "Sharqia",
    "14": "Qalyubia",
    "15": "Kafr El Sheikh",
    "16": "Gharbia",
    "17": "Monufia",
    "18": "Beheira",
    "19": "Ismailia",
    "21": "Giza",
    "22": "Beni Suef",
    "23": "Fayoum",
    "24": "Minya",
    "25": "Assiut",
    "26": "Sohag",
    "27": "Qena",
    "28": "Aswan",
    "29": "Luxor",
    "31": "Red Sea",
    "32": "New Valley",
    "33": "Matrouh",
    "34": "North Sinai",
    "35": "South Sinai",
    "88": "Foreign",
}

def validate_nid(nid: str):
    if len(nid) != 14 or not nid.isdigit():
        raise ValueError("Invalid National ID")

    century = int(nid[0])
    year = int(nid[1:3])
    month = int(nid[3:5])
    day = int(nid[5:7])
    governorate_code = nid[7:9]
    sequence = nid[9:13]

    if century == 2:
        full_year = 1900 + year
    elif century == 3:
        full_year = 2000 + year
    else:
        raise ValueError("Invalid century digit")

    try:
        birth_date = datetime(full_year, month, day).date()
    except ValueError:
        raise ValueError("Invalid date in ID")

    gender = "Male" if int(sequence) % 2 != 0 else "Female"
    governorate = GOVERNORATES.get(governorate_code, "Unknown")

    return {
        "birth_date": birth_date,
        "governorate_code": governorate_code,
        "governorate": governorate,
        "gender": gender
    }
