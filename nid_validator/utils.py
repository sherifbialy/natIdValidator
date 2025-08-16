from datetime import datetime

def _luhn_check_digit(first_13: str) -> int:
    #Luhn's algorithm
    total = 0
    for i, ch in enumerate(reversed(first_13)):
        d = int(ch)
        if i % 2 == 0:
            
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - (total % 10)) % 10

