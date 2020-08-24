import hashlib

import requests


def request_api_data(query_char):
    # Check request status from API and return responses base on first 5 characters of SHA1 Hash of password.
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def password_leaks_count(hashes, hash_checking):
    # Check if remaining characters of SHA1 Hash of password match any leaked one.
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_checking:
            return count


def pwned_api_check(password):
    # Convert password to SHA1 Hash and separate first 5 characters from the rest.
    # Input first 5 characters to API to get responses.
    # Return leaked count.
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5)
    return password_leaks_count(response, tail)


def result(args):
    # Input passwords and return result.
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times...you should change your password.')
        else:
            print(f'{password} was NOT found. Your password is safe...for now.')


def leaked_count(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            return int(count)
        else:
            return False


