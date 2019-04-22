import base64
import math
import sys

def readKeysforVals(fileName):
    with open(fileName, 'r') as myfile:
        b64=myfile.read()
        #Split file directly in half for d/e and n
        val1, val2 = b64[:len(b64)//2], b64[len(b64)//2:]
        x = int.from_bytes(base64.b64decode(val1), "little")
        n = int.from_bytes(base64.b64decode(val2), "little")
        return x,n

def readValsFromKey(key):
    val1, val2 = key[:len(key)//2], key[len(key)//2:]
    x = int.from_bytes(base64.b64decode(val1), "little")
    n = int.from_bytes(base64.b64decode(val2), "little")
    return x,n

"""
    Loads and returns the keys from a file
    Returns: a tuple of the (Key, N) as integers
"""
def load(filename):
    file = open(filename, 'r')
    str = file.read()
    file.close()

    key = str[0:len(str)//2]
    n = str[len(str)//2:]

    key = base64StringToInt(key)
    n = base64StringToInt(n)

    return (key,n)


"""
    Converts a Base64 String to an integer
"""
def base64StringToInt(s):
    return int.from_bytes(base64.b64decode(s.encode()), 'little')

"""
    Converts an integer to a Base64 String
"""
def intToBase64String(n):
    return base64.b64encode(n.to_bytes(math.ceil(n.bit_length()/8), 'little')).decode()


def encryptMessage(key, message):
    e, n = readValsFromKey(key)
    #Convert message to int, encrypt with pow, convert to b64 string
    M = int.from_bytes(str.encode(message), byteorder = "little")
    M = pow(M, e, n)
    bMsg = base64.b64encode(M.to_bytes(math.ceil(M.bit_length()/8), "little"))
    return bMsg.decode()

def decryptMessage(key, cypher):
    d, n = readValsFromKey(key)
    #Convert encrypted message to number, decrypt with pow, convert to string
    cypherText = base64.b64decode(cypher.encode())
    cypherText = int.from_bytes(cypherText, 'little')
    M = pow(cypherText,d,n)
    msg = M.to_bytes(math.ceil(M.bit_length()/8), 'little')
    return msg.decode()


def main():
    d,n = readKeysforVals("private.key")
    e,n = readKeysforVals("public.key")

    try:
        toDo = sys.argv[1]
        #Help Command
        if toDo == "-h":
            print("-e for encryption")
            print("-d for decryption")
            print("-s for signing")
            print("Command format is: python3 rsa.py -e/-d/-s inputFileName outputFileName")
        else:
            fileName = sys.argv[2]
            outputName = sys.argv[3]
            try:
                with open(fileName, 'r') as myfile:
                    try:
                        text=myfile.read()
                        if not text:
                            print("Error: File Empty")
                            exit()
                    
                        if toDo == "-e":
                            x = encryptMessage(e, n, text)
                            print(x, file = open(outputName,'w'))
                        elif toDo == "-d":
                            x = decryptMessage(d, n, text)
                            print(x, file = open(outputName,'w'))
                        elif toDo == "-s":
                            # Signing is simply encrypting with the private key
                            x = encrypt(d, n, text)
                            print(x, file = open(outputName, 'w'))
                        else:
                            #If toDo is not valid
                            raise Exception()
                    except Exception:
                        #If file content is not valid
                        raise Exception()
            except Exception:
                #If file is not valid
                raise Exception()
    except Exception:
        #If Arguments are not valid
        print("Valid paramaters required, use -h for help")

if __name__ == '__main__':
    main()