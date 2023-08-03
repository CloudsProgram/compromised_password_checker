import requests
import hashlib
import sys
"""
This module requires command prompt to run
utility: check to see if our inputted password is already compromised our not

Example 1:
(in commmand promot with correct directory)
python3 compromised_pw_checker.py password123

Expected outcome would be something like:
password123 was found 126927 times... you should change you password
done!


Example 2:
python3 compromised_pw_checker.py 3kmklfsd9
Expected outcome should be:
3kmklfsd9 was NOT found, carry on!
done!

"""
# password is "password1234"
# og hash from sha-1 genarator

# Get data that has the HASH that starts w/ E6B6A
# and use it to compare to our own hash to make sure it doesn't match that confirms that my pw is safe for now


def request_api_data(query_char:str) -> requests.models.Response:
    """
    utility: 
    - takes in first 5 hash characters derived from from our inputted password (query_char)
    - use query_char with the api address to request for current compromised hashes that
    matches our own password's first 5 hash character
    - if requested successfully it should return the requested Hashes
    """
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)

    # if status code is 400 = the request to the API did not work
    # if status code is 200 = API request works
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check API and try again')
    return res


def get_password_leaks_count(hashes_got:requests.models.Response, my_pw_hash_check:str) -> int:
    """
    utlity:
    - orginal string from the retrived hashes have the amount of times that specific hash has
    been compromised
    - we break that string up into the compromised hash, and the amount of times compromised
    - if any of the compromised hash[5:] matches our hash[5:], then it means that our password has already
    been compromised
    - return amount of times compromised or return 0 if not compromised
    """
    hashes = (line.split(':') for line in hashes_got.text.splitlines())
    for h, count in hashes:

        # compare hash[5:] from compromised to my password hash[5:]
        if h == my_pw_hash_check:
            return count
    return 0


def pwned_api_check(password:str) -> int:
    """
    utility:
    - take input passsword and convert it to its respective hash (sha-1)
    - get the first 5 characters of our pw hash, and rest of the characters of it.
    - input the first 5 char of our pw hash into the function that gets us a collection of
    compromised hashes that matches our 1st 5 char of our pw hash.
    - we then input the collection and [5:] of our pw hash to a function that count amount of
    times our passsword has been undermined
    """
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_five_hash, tail = sha1password[:5], sha1password[5:]


    response = request_api_data(first_five_hash)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f'{password} was found {count} times... you should change you password')
        else:
            print(f'{password} was NOT found, carry on!')
    print('Done!')
    


# check any arguments of chekcmypassword.py
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
