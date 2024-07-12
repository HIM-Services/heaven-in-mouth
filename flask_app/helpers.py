import re

def validate_email(email: str) -> bool:
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}"
    #Check if email matches the pattern
    if (re.fullmatch(pattern, email)):
        #Email is valid
        return True
    else:
        #Email is invalid
        return False
    
def validate_phone(phone: str) -> bool:
    pattern = r"^[0-9]{5,10}$"
    if (re.fullmatch(pattern, phone)):
        #Phone is valid
        return True
    else:
        #Phone is invalid
        return False
    