def caesar():
    return '''
    def encrypt(str, key):
    cipher =''
    for i in range(len(str)):
        char = str[i] 

        if (char.isupper()):
            cipher += chr((ord(char) - 65 + key) % 26 + 65)

        else:
            cipher += chr((ord(char) - 97 + key) % 26 + 97)

    return cipher

    def decrypt(cipher, key):
        plain =''
        for i in range(len(cipher)):
            char = cipher[i] 

            if (char.isupper()):
                plain += chr((ord(char) - 65 - key) % 26 + 65)

            else:
                plain += chr((ord(char) - 97 - key) % 26 + 97)

        return plain

    text = input("Enter text: ")
    key = int(input("Enter key: "))
    cipher = encrypt(text, key)

    print(f"Cipher text is: {cipher}")
    print(f"Plain text is: {decrypt(cipher, key)}")
    '''

def digital_sig():
    return '''
    import math
    import random
    def gcd(x,y):
        if not(y):
            return x
        else:
            return gcd(y, x%y)

    def genrateKeys(p,q):
        n = p*q
        et = (p - 1) * (q - 1)
        d=0
        while(1):
            e = 313
            if(gcd(e,et) == 1):
                break
        
        while(1):
            if((e * d) % et == 1):
                break
            d+=1
        
        return [[e,n], [d,n]]

    def cipherFunction(arr, key):
        for i in range(len(arr)):
            arr[i] = chr(int((arr[i]**key[0])%key[1]))
        
        return arr

    def encodeText(str, key):
        # arr = str.split()
        arr = []
        for i in str:
            arr.append(ord(i)) 
        
        return [str, "".join(cipherFunction(arr,key))]


    def decodeText(sign, key):
        arr = []
        for i in sign[1]:
            arr.append(ord(i)) 
        
        return [sign[0], "".join(cipherFunction(arr, key)) == sign[0]]


    str = "Saloni Modi 20BCP052"
    [enkey,dekey] =  genrateKeys(823, 953)

    encodeStr = encodeText(str, enkey)
    print("Sign :", encodeStr[1], '\nSEND: ','\n',encodeStr[0])


    decodeStr = decodeText(encodeStr, dekey)
    print("RECEIVE :", decodeStr[1], '\n',decodeStr[0]  if decodeStr[1] else "")
    '''

def double_transpo():
    return '''
    import numpy as np

    def Create(plaintext,length):
        
        letters=list(plaintext.lower().replace(" ",""))
        extra_to_add=length-(len(letters)%length)
        letters.extend(["X" for x in range(extra_to_add)])

        m = len(letters)//length
        n = length
        
        return((np.array(letters).reshape(m,n)))

    def Encrypt(matrix,key):
        key=list(map(int,key))
        temp_dict={}
        for k in range(len(key)):
            temp_dict[key[k]]=list(matrix[:,k])
        
        final=[]
        for k in range(1,len(key)+1):
            final.extend(temp_dict[k])
        
        return("".join(final))


    def Decrypt(text,key):
        length=len(text)
        part=length//len(key)
        
        matrix=[]

        for i in range(0, length, part):  
            matrix.append(text[i:i+part])
        
        temp_dict={}
        for k in range(1,len(key)+1):
            temp_dict[k]=matrix[k-1]

        final=[]
        for k in range(len(key)):
            col=temp_dict[int(key[k])]
            final.append([x for x in col])

        final=np.array(final).T.reshape(1,length)
        
        return(("".join(final[0])).replace("X",""))

    plaintext="Hello good morning goodbye"
    key="987654123"

    matrix=(Create(plaintext,len(key)))
    encrypted=(Encrypt(matrix,key))

    encrypted_matrix=(Create(encrypted,len(key)))
    double_encrypted=(Encrypt(encrypted_matrix,key))

    print("Encrypted: ",encrypted)
    print("Double Encrypted: ",double_encrypted)

    decrypted=Decrypt(double_encrypted,key)
    double_decrypted=Decrypt(decrypted,key)
    print("Decrypted: ",decrypted)
    print("Double Decrypted: ",double_decrypted)
    '''

def hill():
    return '''
    import math
    from sympy import *

    plaintext = input("Enter plaintext: ").upper()
    key = input("Enter key: ").upper()

    if len(plaintext) < len(key):
        plaintext+=(len(key) - len(plaintext))*"X"
    else:
        plaintext = plaintext[:len(key)]

    matrix_lengthKey = (math.sqrt(len(key)))
    matrix_lengthPlaintext = (math.sqrt(len(plaintext)))

    tableKey = [[0 for j in range(0, int(matrix_lengthKey))]
                for i in range(0, int(matrix_lengthKey))]

    j = 0
    i = 0

    for k in key:
        if j >= int(matrix_lengthKey):
            j = 0
            i += 1
        tableKey[i][j] = ord(k) % 65
        j += 1

    tablePlaintext = [[0 for j in range(0, int(matrix_lengthPlaintext))]
                    for i in range(0, int(matrix_lengthPlaintext))]

    j = 0
    i = 0

    for k in plaintext:
        if j >= matrix_lengthPlaintext:
            j = 0
            i += 1
        tablePlaintext[i][j] = ord(k) % 65
        j += 1

    result = [[0 for j in range(0, int(matrix_lengthPlaintext))]
            for i in range(0, int(matrix_lengthKey))]

    for j in range(len(tablePlaintext)):
        for i in range(len(tableKey)):
            sum = 0
            for k in range(len(tableKey[i])):
                sum += (tableKey[i][k]*tablePlaintext[j][k])
                result[j][i] = sum % 26
    encryptedText = ""

    for i in range(len(result)):
        for j in range(len(result[0])):
            encryptedText += (chr(result[i][j] + 65))
            
    print()
    print(f"Encryption: {encryptedText}")
    tempMatrix = [[0 for i in range(0,len(tableKey))] for j in range(0,len(tablePlaintext))]

    for i in range(len(tableKey)):
        for j in range(len(tableKey[0])):
            tempMatrix[j][i] = tableKey[i][j]

    A = Matrix(tempMatrix)
    tempMatrix = A.adjugate().T.tolist()
    determinant = A.det()%26
    multInverse = 0
    for i in range(1,27):
        if (determinant*i)%26 == 1:
            multInverse = i
            break
    else:
        print("No Possible Multiplcative Inverse")
        exit()

    for i in range(len(tempMatrix)):
        for j in range(len(tempMatrix[0])):
            tempMatrix[i][j] = multInverse*tempMatrix[i][j]%26

    j = 0
    i = 0
    for k in encryptedText:
        if j >= matrix_lengthKey:
            j = 0
            i += 1
        tablePlaintext[i][j] = ord(k) % 65
        j += 1

    for j in range(len(tablePlaintext)):
        for i in range(len(tempMatrix)):
            sum = 0
            for k in range(len(tempMatrix[i])):
                sum += (tempMatrix[i][k]*tablePlaintext[j][k])
                result[j][i] = sum % 26

    decryptedText = ""
    for i in range(len(result)):
        for j in range(len(result[0])):
            decryptedText += (chr(result[i][j] + 65))
    print(f"Decryption: {decryptedText}")
    '''

def playfair_5x5():
    return '''
    def create_matrix(key):
        key = key.upper()
        matrix = [[0 for i in range(5)] for j in range(5)]
        letters_added = []
        row = 0
        col = 0
        for letter in key:
            if letter not in letters_added:
                matrix[row][col] = letter
                letters_added.append(letter)
            else:
                continue

        for letter in range(65,91):
            if letter == 74:
                continue
            else:
                if chr(letter) not in letters_added:
                    letters_added.append(chr(letter))

        index = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = letters_added[index]
                index += 1
        
        return matrix

    def separate_same_letters(message):
        index = 0
        while (index<len(message)):
            l1 = message[index]
            if index == len(message)-1:  # for last element if odd number
                message = message + 'X'
                index += 2
                continue
            l2 = message[index+1]
            if l1==l2:
                message = message[:index+1] + "X" + message[index+1:]
            index +=2   
        return message

    def indexOf(letter,matrix):
        for i in range (5):
            try:
                index = matrix[i].index(letter)
                return (i,index)
            except:
                continue

    def playfair(key, message, encrypt=True):
        inc = 1
        if encrypt==False:
            inc = -1
        matrix = create_matrix(key)
        message = message.upper()
        message = message.replace(' ','')    
        message = separate_same_letters(message)
        cipher_text=''
        for (l1, l2) in zip(message[0::2], message[1::2]):
            row1,col1 = indexOf(l1,matrix)
            row2,col2 = indexOf(l2,matrix)
            if row1==row2: # the letters are in the same row
                cipher_text += matrix[row1][(col1+inc)%5] + matrix[row2][(col2+inc)%5]
            elif col1==col2: # the letters are in the same column
                cipher_text += matrix[(row1+inc)%5][col1] + matrix[(row2+inc)%5][col2]
            else:  # the letters are in a different row and column
                cipher_text += matrix[row1][col2] + matrix[row2][col1]
        
        return cipher_text

    print (f"Encrypted text: {playfair('hardkey', 'Hello Good morning How are you', True)}")
    print (f"Decrypted text: {playfair('hardkey', 'EGMWGQOUSHGSKLLGOEQURDYBUH', False)}")
    '''

def railfence():
    return '''
    def encryptRailFence(text, key):
        rail = [['\n' for i in range(len(text))]
                    for j in range(key)]
        dir_down = False
        row, col = 0, 0
        for i in range(len(text)):
            if (row == 0) or (row == key - 1):
                dir_down = not dir_down
            rail[row][col] = text[i]
            col += 1

            if dir_down:
                row += 1
            else:
                row -= 1
        result = []
        for i in range(key):
            for j in range(len(text)):
                if rail[i][j] != '\n':
                    result.append(rail[i][j])
        return("" . join(result))

    def decryptRailFence(cipher, key):
        rail = [['\n' for i in range(len(cipher))]
                    for j in range(key)]
        dir_down = None
        row, col = 0, 0
        for i in range(len(cipher)):
            if row == 0:
                dir_down = True
            if row == key - 1:
                dir_down = False
            rail[row][col] = '*'
            col += 1

            if dir_down:
                row += 1
            else:
                row -= 1
        index = 0
        for i in range(key):
            for j in range(len(cipher)):
                if ((rail[i][j] == '*') and
                (index < len(cipher))):
                    rail[i][j] = cipher[index]
                    index += 1
        result = []
        row, col = 0, 0
        for i in range(len(cipher)):
            if row == 0:
                dir_down = True
            if row == key-1:
                dir_down = False

            if (rail[row][col] != '*'):
                result.append(rail[row][col])
                col += 1

            if dir_down:
                row += 1
            else:
                row -= 1
        return("".join(result))

    print(encryptRailFence("hellogoodmorning", 5))
    print(encryptRailFence("HELLOUNIVERSEGOODMORNING", 6))
    print(decryptRailFence("hdeomgloonlgrion", 5))
    print(decryptRailFence("HRNEESRILVEONLIGMGONODUO", 6))
    '''

def rsa():
    return '''
    from math import gcd
    import random

    def RSA_Encryption(M,p,q):
        n=p*q
        phin=(p-1)*(q-1) 

        l=[]
        for i in range(2,phin): 
            if gcd(phin,i)==1:
                l.append(i)
        e=random.sample(l,1)[0] 
        d=1
        while (e*d)%phin!=1: 
            d=d+1
        C=1
        for i in range(e):
            C=((C*M)%n)%n
        return C,n,e,d


    def RSA_Decryption(C,n,e,d):
        m=1
        for i in range(d): 
            m=((m*C)%n)%n
        return m

    M=int(input('Enter a message: '))
    p=int(input('Enter a prime number: '))
    q=int(input('Enter a prime number: '))
    C,n,e,d= RSA_Encryption(M,p,q)
    print('Your encrypted message is: ',C)
    print('Your decrypted message is: ',RSA_Decryption(C,n,e,d))
    '''

def vigenere():
    return '''
    plaintext = input("Enter the plaintext: ").replace(" ", "").upper()
    key = input("Enter the key: ").replace(" ", "").upper()
    repeatKey = key
    while len(key) <= len(plaintext):
        key += repeatKey
    encryption = ""
    for i in range(0, len(plaintext)):
        a1 = (ord(plaintext[i]) % 65)
        a2 = (ord(key[i]) % 65)
        encryption += (chr(((a1+a2) % 26)+65))
    print(f"Encryption: {encryption}")
    decryption = ""
    for i in range(0, len(plaintext)):
        a1 = (ord(encryption[i]) % 65)
        a2 = (ord(key[i]) % 65)
        decryption+=(chr(((a1-a2) % 26)+65))
    print(f"Decryption: {decryption}")
    '''

def playfair_6x6():
    return '''
    import numpy as np
    def Matrix(key):
        k=''
        for i in key.upper():
            if i not in k:
                k+=i
        for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            if j not in k:
                k+=j
        return np.array([list(k)]).reshape(6,6)

    def digram(a):
        k=""
        a = a.replace(" ","").upper()
        i=0
        while i<len(a):
            try:
                if a[i]!=a[i+1]:
                    k+=f"{a[i]+a[i+1]}"
                    i+=2
                else:
                    k+=f"{a[i]}X"
                    i+=1
            except:
                k+=f"{a[i]}X"
                i+=1
        return list(k)

    def search(matrix,element):
        for i in range(6):
            for j in range(6):
                if matrix[i][j]==element:
                    return i,j

    def encryption(plain_text,key):
        cipher_text=''
        d=digram(plain_text)
        v=Matrix(key)
        for i in range(0,len(d),2):
            a=d[i:i+2]
            r1,c1 = search(v,a[0])
            r2,c2 = search(v,a[1])
            if r1 == r2:
                first = v[r1][0] if c1+1 > 5 else v[r1][c1+1]
                second = v[r2][0] if c2+1 > 5 else v[r2][c2+1]
                cipher_text=cipher_text+first+second
            elif c1 == c2:
                first = v[0][c1] if r1+1 > 4 else v[r1+1][c1]
                second = v[0][c2] if r2+1 > 4 else v[r2+1][c2]
                cipher_text=cipher_text+first+second
            else:
                first,second =v[r1][c2],v[r2][c1]
                cipher_text=cipher_text+first+second
        return cipher_text
        
    def decryption(cipher_text,key):
        decrypted_text=''
        v=Matrix(key)
        for i in range(0,len(cipher_text),2):
            a=cipher_text[i:i+2]
            r1,c1 = search(v,a[0])
            r2,c2 = search(v,a[1])
            if r1 == r2:
                first = v[r1][-1] if c1-1 < 0 else v[r1][c1-1]
                second = v[r2][-1] if c2-1 < 0 else v[r2][c2-1]
                decrypted_text=decrypted_text+first+second
            elif c1 == c2:
                first = v[-1][c1] if r1-1 < 0 else v[r1-1][c1]
                second = v[-1][c2] if r2-1 < 0 else v[r2-1][c2]
                decrypted_text=decrypted_text+first+second
            else:
                first,second = v[r1][c2],v[r2][c1]
                decrypted_text=decrypted_text+first+second
        return decrypted_text

    plain_text=input('Enter a text: ')
    print(digram(plain_text))
    key=input('Enter a key: ')
    print(Matrix(key))
    cipher_text=encryption(plain_text,key)
    print('Ciphered text: ',cipher_text)
    print('Decrypted text: ',decryption(cipher_text,key))
    '''

def help():
    return '''
    caesar()
    digital_sig()
    double_transpo()
    hill()
    playfair_5x5()
    railfence()
    rsa()
    vigenere()
    playfair_6x6()
    '''