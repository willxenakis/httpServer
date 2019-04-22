import random
import sys
import math
from fractions import gcd
import base64
import time

# Replacement range function
def yRange(start, stop, step=1):
    while start<stop:
        yield start
        start += step

#Returns a prime of size 2^numBits our larger (Mr. Sea helped)
def getPrime(numBits):
    upperBound = 2**(numBits+1)
    lowerBound = 2**(numBits)

    num = random.randrange(lowerBound, upperBound, 1)

    def isPrime(num):
        if num == 2:
            return True
        if not num & 1:
            return False
        
        return pow(2,num-1, num)==1

    while not isPrime(num):
        num = num + 2
        while num.bit_length() > numBits:
            num = num // 2

            if (not num & 1) and (num != 2):
                num = num+1
    return num

# Unused function
def generatePrimes(n): 
    # Sieve technique that is extremly inneficient
    prime = [True]*(n+1)
    p = 2
    while (p * p <= n): 
        if (prime[p] == True):  
            for i in range(p * 2, n+1, p): 
                prime[i] = False
        p += 1
    nums = []
    i = pow(2,23)
    while(i<len(prime)):
        if prime[i]:
            nums.append(i)
        i=i+1
    return (random.choice(nums),random.choice(nums))

# Unused function
def bruteForce(totientN, e):
    #Choose random values into on is valid
    while True:
        # d = 5
        d = random.randrange(5, totientN, 1)
        if ((d*e) % totientN == 1):
            return d
            break

# Uses extended Euclids algorithm iterratively to find d (copied from internet)
def findDEuclid(totientN, e):
    x, y, u, v = 0, 1, 1, 0
    tempTotient = totientN
    while totientN!=0:
        q, r = e//totientN, e%totientN
        m, n = x - u * q, y - v * q
        e, totientN, x, y, u, v = totientN, r, u, v, m, n
    return y % tempTotient

#Puts all functions together to find d, e, n, and totientN and convert them into base64 and print them to key files
def publicPrivate(p,q):
    n = p*q
    totientN=(p-1)*(q-1)
    e = 1
    #Generate random values for e in range 2^numbits < e < totientN until gcd of e and totientN is 1
    #Then a valid e has been found
    while(True):
        e = random.randrange(pow(2, 3000), totientN, 1)
        if math.gcd(e,totientN) == 1:
            break
    d = findDEuclid(totientN, e)
    # d = bruteForce(totientN, e)
    
    tempE = e.to_bytes(math.ceil(e.bit_length()/8), "little")
    eBase64 = base64.b64encode(tempE)
    tempN = n.to_bytes(math.ceil(n.bit_length()/8), "little")
    nBase64 = base64.b64encode(tempN)
    tempD = d.to_bytes(math.ceil(d.bit_length()/8), "little")
    dBase64 = base64.b64encode(tempD)
    
    eBase64 = eBase64.decode()
    nBase64 = nBase64.decode()
    dBase64 = dBase64.decode()
    
    print(eBase64 + nBase64, file = open('Bpublic.key','w'))
    print(dBase64 + nBase64, file = open('Bprivate.key','w'))

# start = time.time()
val1 = getPrime(2048)

val2 = getPrime(2048)

publicPrivate(val1, val2)
# end = time.time()
# print(end - start)