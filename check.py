def check_email(enter):
    try:
        username, domain = enter.split("@")
        if username != "" and domain != "":
            return True
        else:
            return False
    except ValueError:
        return False
    
def check_password(password):
    # number, letter(capital+lower) & special letter
    number = False
    capital = False
    lower_letter = False
    special = False
    for letter in password:
        if letter.isdigit():
            number = True
        elif letter.isalpha() and letter.islower():
            lower_letter = True
        elif letter.isalpha() and letter.isupper():
            capital = True
        elif letter.isascii():
            special = True
            
    
            
