# Names: Luisa Escosteguy, PJ Sangvong
import hashlib
import binascii
import random

dict = {}
dict_two_word = {}

def hash_string(word):
    '''
    Type conversions and hash
    '''
    encoded_password = word.encode('utf-8')
    hasher = hashlib.sha256(encoded_password)
    digest = hasher.digest() 
    digest_as_hex = binascii.hexlify(digest)
    digest_as_hex_string = digest_as_hex.decode('utf-8')
    return digest_as_hex_string
 

def build_dictionary():
    '''
    Build the dictionary used in part 1, key is hash, value is password
    '''
    words = [line.strip().lower() for line in open('temp/words.txt')]
    for word in words:
        digest_as_hex_string = hash_string(word)
        if digest_as_hex_string not in dict:
            dict[digest_as_hex_string] = word


def build_two_word_dict():
    '''
    We tried this approach for part 2, but it takes too long
    '''
    words = [line.strip().lower() for line in open('temp/words.txt')]
    for word1 in words:
        for word2 in words:
            word = word1+word2
            digest_as_hex_string = hash_string(word)
            if digest_as_hex_string not in dict:
                dict_two_word[digest_as_hex_string] = word


def crack_password(password_path, output_name, dict):
    passwords = [line.strip().lower() for line in open(password_path)]
    with open(output_name, 'w') as f:
        for password in passwords:
            hash = password.split(":",2) 
            if hash[1] in dict:
                f.write(hash[0]+":"+dict[hash[1]]+"\n")


def randomized_crack(password_path, output_name):
    '''
    Randomly pick some words to hash together and see if we get a match
    '''
    words = [line.strip().lower() for line in open('temp/words.txt')]
    passwords = [line.strip().lower() for line in open(password_path)]
    passwords_dict = {}
    with open(output_name, 'w') as f:
        for password in passwords:
            hash = password.split(":",2) 
            passwords_dict[hash[1]] = hash[0]
        
        c = 0
        for _ in range(8000000000):
            rand_word1, rand_word2 = random.choices(words, k=2)
            rand_word = rand_word1 + rand_word2
            rand_hash = hash_string(rand_word)
            if rand_hash in passwords_dict:
                c += 1
                print("Count: "+str(c)+" "+passwords_dict[rand_hash]+":"+rand_word+"\n")
                f.write(passwords_dict[rand_hash]+":"+rand_word+"\n") 


def salted_crack(password_path, output_name):
    '''
    Go through each salt and use that salt to hash with all the words until we get 
    the password
    '''
    words = [line.strip().lower() for line in open('temp/words.txt')]
    passwords = [line.strip().lower() for line in open(password_path)]
    num_hash = 0

    with open(output_name, 'w') as f:
        for password in passwords:
            password_colon_split = password.split(":",2)
            password_dollar_split = password_colon_split[1].split("$")
            user = password_colon_split[0]
            salt = password_dollar_split[2]
            hash = password_dollar_split[3]

            # all the salts are unique, so no need to keep any hash in memory
            for word in words: 
                digest_as_hex_string = hash_string(salt+word)
                num_hash += 1
                if digest_as_hex_string == hash:
                    f.write(user+":"+word+"\n")
                    break # stops looking for password when finds one

    print(f'created {num_hash} hashes')

def part1():
    '''
    Cracks unsalted one-word passwords
    '''
    build_dictionary()
    crack_password('temp/password1.txt', 'cracked1.txt', dict)


def part2():
    '''
    Cracks unsalted two-word passwords
    '''
    # build_two_word_dict() # takes too long
    # crack_password('temp/password2.txt', 'cracked2.txt', dict_two_word)
    randomized_crack('temp/password2.txt', 'cracked2.txt')


def part3():
    '''
    Cracks salted one-word passwords
    '''
    salted_crack('temp/password3.txt', 'cracked3.txt')

def sanity_check():
    salt = "73f5c390"
    hash = "6b5b88886d9fcd76e5c4dceafb0069cb969d4f63d331793ae78b1f9b99bdee41"
    word = "moose"
    digest_as_hex_string = hash_string(salt+word)
    print(digest_as_hex_string == hash)


if __name__ == '__main__':
    # part1()
    part2()
    # sanity_check()
