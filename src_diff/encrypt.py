#RSA encryption

import random
import time

#Determining the greatest common divisor
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def quick_pow(x,y,n):
    if y == 0:
        return 1
    if y == 1:
        return int(x)**y%n
    if y%2 == 0:
        return (quick_pow(int(x),y//2,n)**2)%n
    return (x * (quick_pow(int(x),y//2,n)**2)%n)%n

#Determining the the multiplicative inverse of two relative p[rime numbers
def find_multiplicative_inverse(a,b):
    if gcd(a,b) != 1:
        return None
    i,j,k = 1,0,a
    x,y,z = 0,1,b
    while z != 0:
        q = k//z
        x,y,z,i,j,k = (i-q*x), (j-q*y),(k-q*z),x,y,z
    return i % b

#Determining whether the number is a prime number in O(n**0.5) runnning time
def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime_list(a,b):
    prime_list = []
    for i in range(a,b):
        if is_prime(i):
            prime_list.append(i)
    return prime_list

prime_list = generate_prime_list(100,10000)

#generate public key and private key
def generate_key():
    p = random.choice(prime_list)
    q = random.choice(prime_list)
    while p == q:
        q = random.choice(prime_list)
    n = p*q
    # calculate euler function phi(n)
    phi = (p-1) * (q-1)
    # Choose an integer e that is relative prime with phi(n)
    e = random.randint(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    # Use Extended Euclid's Algorithm to generate the private key
    d = find_multiplicative_inverse(e, phi) #d = (p-1)*(q-1) - 1
    public_key = (e,n)
    private_key = (d,n)
    return public_key, private_key

#encryption
def encryption(message,public_key):
    e,n = int(public_key[0]), int(public_key[1])
    encrypted_number = []
    #message += "xxx"
    for i in message:
        encrypted_number.append(quick_pow(ord(i),e,n))
    print(str(encrypted_number))
    return str(encrypted_number)

#decryption
def decryption(message,private_key):
    d,n = int(private_key[0]), int(private_key[1])
    decrypted_message = []
    if len(message) > 0:
        message = str(message)
    message = message[1:-1]
    message = message.split(",")

    for i in message:
        t = int(i)
        decrypted_message.append(chr(quick_pow(t,d,n)))
    message_text = "".join(decrypted_message)
    return message_text

def main():
    public_key, private_key = generate_key()
    print(public_key, private_key)
    message = "Hi"
    print(message)
    encrypted_message = encryption(message, public_key)
    print('Here is the encrypted message: ', end = '')
    print(encrypted_message)
    received_message = decryption(encrypted_message, private_key)
    print('Here is the message you receive: ' +  received_message)

if __name__ == "__main__":
    main()
