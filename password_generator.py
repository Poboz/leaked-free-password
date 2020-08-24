import re
import secrets
import string

from password_project.checkmypass import leaked_count


def password_length():
    while True:
        try:
            length = int(input("Please specify desired password length (must be 6 or higher): "))
            if length >= 6:
                return length
            else:
                print('Password length is too short.')
        except ValueError:
            print('Please enter a number.')


def password_generator(length, option):
    password_universe = choice_based_universe(option)
    random_password = (secrets.choice(password_universe) for _ in range(length))
    random_password_result = ''.join(random_password)
    return print(f'Your secured password: {random_password_result}')


def secured_password_generator(length, option):
    password_universe = choice_based_universe(option)
    if length == 6 and re.compile(r"^[0-9]*$").fullmatch(password_universe):
        while True:
            try:
                max_leak_count = int(input("Please specify acceptable leaked counts: "))
                if max_leak_count >= 0:
                    break
                else:
                    print('Leaked counts must be higher than 0.')
            except ValueError:
                print('Please enter a number.')
    else:
        max_leak_count = 0
    while True:
        random_password = (secrets.choice(password_universe) for _ in range(length))
        random_password_result = ''.join(random_password)
        if leaked_count([random_password_result]) > max_leak_count:
            continue
        else:
            break
    with open('./password_project/password.txt', 'a') as file:
        file.write(random_password_result+'\n')
    return print(f'Your secured password: {random_password_result}')


def password_option():
    option = input('Enable password option (Y/N): ').upper()
    if option == 'N':
        return ['Y', 'Y', 'Y', 'Y']
    else:
        while True:
            upper_letters_option = input('Capitalized letters included (Y/N): ').upper()
            lower_letters_option = input('Lower letters included (Y/N): ').upper()
            numbers_option = input('Numbers included (Y/N): ').upper()
            punctuations_option = input('Punctuations included (Y/N): ').upper()
            try:
                answers = [upper_letters_option, lower_letters_option, numbers_option, punctuations_option]
                for ans in answers:
                    if ans == 'Y' or ans == 'N':
                        continue
                    else:
                        raise ValueError
                return answers
            except ValueError:
                print('Please enter Y or N only.')


def choice_based_universe(choice_option):
    upper_letters = string.ascii_uppercase if choice_option[0] == 'Y' else ''
    lower_letters = string.ascii_lowercase if choice_option[1] == 'Y' else ''
    numbers = string.digits if choice_option[2] == 'Y' else ''
    punctuations = string.punctuation if choice_option[3] == 'Y' else ''
    return f'{upper_letters}{lower_letters}{numbers}{punctuations}'


if __name__ == '__main__':
    secured_password_generator(password_length(), password_option())
