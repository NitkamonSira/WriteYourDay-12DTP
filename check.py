def check_email(enter):
    """Basic check for whether the input is email or not.
    Check that the input contains '@' or not and check that there are some things before and after the sign.

    Args:
        enter (str): The input that the user enters as an email.

    Returns:
        bool: True for the input that pass the basic check and False for not
    """
    try:
        username, domain = enter.split("@")
        if username != "" and domain != "":
            return True
        else:
            return False
    except ValueError:
        return False
    
def check_password(password):
    """Check the input taken met the minimum requirements for password.

    Args:
        password (str): The input that the user enters as a password.

    Returns:
        bool: True for the input that meet the requirement, False for not met
    """
    condition = 0
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
            
    if number:
        condition += 1
    if capital:
        condition += 1
    if lower_letter:
        condition += 1
    if special:
        condition += 1
    
    if len(password) >= 8 and condition >= 3:
        return True
    else:
        return False
    
            
