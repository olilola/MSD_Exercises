# Large Prime Generation for RSA
import random
import logging
 
# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def nBitRandom(n):
    '''Create a random number with n bits'''
    return random.randrange(2**(n-1)+1, 2**n - 1)
 
 
def getLowLevelPrime(n):
    '''Generate a prime candidate divisible by first primes'''
    while True:
        # Obtain a random number
        pc = nBitRandom(n)
 
        # Test divisibility by pre-generated
        # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else:
            return pc
 
 
def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1)
 
    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                return False
        return True
 
    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True
 

def get_prime_slow(n):
  '''Generates a prime number (with n bits) in a slow way'''
  # Repeat until a number satisfying 
  # the test isn't found 
  while True:  
   
    # Obtain a random number 
    prime_candidate = nBitRandom(n)
    max_divisor = int((prime_candidate+1)/2)
    isPrime = True
   
    for divisor in range(2, max_divisor):  
      if prime_candidate % divisor == 0:
        isPrime = False 
        break
        # If no divisor found, return value 
    
    if isPrime:
      return prime_candidate


def get_prime_fast(n):
    '''Creates a prime number (with n bits) in a fast way'''
    while True:
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate


def gcd(a, b):
    '''Calculates the GCD (greatest common divisor) of two given numbers'''
    while b != 0:
        a, b = b, a % b
    return a


def generate_rsa_keypair(p, q, e):
    '''Generates a RSA key pair with the given prime numbers'''
    n = p * q
    phi = (p-1) * (q-1)
    
    logging.debug(n)
    logging.debug(phi)
    logging.debug(e)

    if e is None:
        e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = pow(e, -1, phi)

    return e, d, n


def encrypt(public_key, plaintext):
    'Encrypt a message with a given public key'
    key, n = public_key
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher


def decrypt(private_key, ciphertext):
    'Decrypt a message with a given key'
    key, n = private_key
    aux = [str(pow(char, key, n)) for char in ciphertext]
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


def brute_force_hacking(n):
    '''brute force prime number factorization'''
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def decrypt_with_public_key(n, e, ciphertext):
    '''Decrypt a message using brute force to find the private key from the public key'''
    # Factorize n to find p and q
    factors = brute_force_hacking(n)
    if len(factors) != 2:
        raise ValueError("Failed to factorize n into two primes")
    
    p, q = factors
    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)
    private_key = (d, n)
    return decrypt(private_key, ciphertext)

def decrypt_2(private_key, ciphertext):
    'Decrypt a message with a given key'
    key, n = private_key
    plain = []
    for char in ciphertext:
        decrypted_char = pow(char, key, n)
        # Convert the decrypted integer to bytes
        decrypted_bytes = decrypted_char.to_bytes((decrypted_char.bit_length() + 7) // 8, byteorder='big')
        # Decode the bytes to obtain the plaintext character
        plain.append(decrypted_bytes.decode('utf-8', errors='ignore'))
    return ''.join(plain)


if __name__ == '__main__':

  # logging.basicConfig(level=logging.DEBUG)
    # PK 347185791680057079, 16802743328604983
 
    e = 3857915162579603
    n = 35934062448514481
 
    #print(brute_force_hacking(n))  # [150944557, 238061333]
 
    p = 150944557
    q = 238061333
 
    e2, d2, n2 = generate_rsa_keypair(p, q, e)
 
    # print(generate_rsa_keypair (p, q, e)) #(3857915162579603, 26012068694834795, 35934062448514481)
 
    enc_message = [
        24322083524468281,
        35507326732878763,
        31400689936145418,
        31400689936145418,
        24178824277506292,
        2905982487084417,
        19330968508506227,
        35507326732878763,
        31400689936145418,
        2905982487084417,
        6214242669149926,
        24178824277506292,
        2905982487084417,
        6214242669149926,
        8494066427442995,
        4050037809818744,
        8889814276547977,
        3331179209893932,
        28642392891932956,
        8107708887580794,
        10847748137261138,
        2905982487084417,
        20383315096743517,
        35507326732878763,
        8866751532625061,
        2905982487084417,
        3331179209893932,
        31400689936145418,
        8107708887580794,
        2905982487084417,
        5645747285816569,
        35507326732878763,
        1685070066111050,
        2905982487084417,
        31400689936145418,
        8107708887580794,
        3331179209893932,
        2631842245135151,
        24178824277506292,
        2905982487084417,
        8889814276547977,
        35507326732878763,
        2905982487084417,
        18556768846845797,
        35507326732878763,
        2905982487084417,
        19330968508506227,
        35507326732878763,
        31400689936145418,
        2905982487084417,
        3331179209893932,
        2905982487084417,
        21733787468085948,
        31400689936145418,
        8107708887580794,
        3331179209893932,
        28642392891932956,
        26616902325000265,
    ]
 
    private_key = (d2, n2)
 
    # Decrypt the message
    decrypted_message = decrypt(private_key, enc_message)
 
    # Print the decrypted message
    print("Decrypted message:", decrypted_message)
 
    # THIS Exercice is finished!
 