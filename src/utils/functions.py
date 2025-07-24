def format_phone_number(phone):
    if not phone:
        return None
    digits_only = "".join(char for char in phone if char.isdigit())
    if len(digits_only) < 10:
        return None
    if len(digits_only) == 10:
        return "7" + digits_only
    elif len(digits_only) == 11:
        if digits_only.startswith("8"):
            return "7" + digits_only[1:]
        elif digits_only.startswith("7"):
            return digits_only
        else:
            return digits_only
    else:
        return digits_only