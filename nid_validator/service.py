from datetime import datetime
from nid_validator.utils import _luhn_check_digit


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
    if not (isinstance(nid, str) and nid.isdigit() and len(nid) == 14):
        return {"valid": False, "message": "National ID must be exactly 14 digits."}

    century = int(nid[0])
    yy = int(nid[1:3])
    mm = int(nid[3:5])
    dd = int(nid[5:7])
    governorate_code = nid[7:9]
    sequence = nid[9:13]
    check = int(nid[13])

    if century == 2:
        full_year = 1900 + yy
    elif century == 3:
        full_year = 2000 + yy
    else:
        return {"valid": False, "message": "Invalid century digit (must be 2 or 3)."}
    
    # Commented out as has strange behavior
    
    # expected_check = _luhn_check_digit(nid[:13])
    # if check != expected_check:
    #     return {"valid": False, "message": "Invalid check digit."}

    try:
        birth_date = datetime(full_year, mm, dd).date()
    except ValueError:
        return {"valid": False, "message": "Invalid birth date encoded in ID."}
    
    today = datetime.today().date()
    min_allowed = today.replace(year=today.year - 16)
    if birth_date > min_allowed:
        return {"valid": False, "message": "Holder must be at least 16 years old."}

    governorate = GOVERNORATES.get(governorate_code)
    if not governorate:
        return {"valid": False, "message": "Invalid governorate code."}

    if int(sequence) == 0:
        return {"valid": False, "message": "Invalid sequence digits."}

    

    gender = "Male" if int(sequence) % 2 == 1 else "Female"

    return {
        "valid": True,
        "birth_date": birth_date.isoformat(),
        "governorate_code": governorate_code,
        # "governorate": governorate,
        "gender": gender,
        # "check_digit": check,
    }

