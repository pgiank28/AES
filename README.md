# AES
This is a very simple AES imlementation in python.
It's a script that can be used by another python script by importing it
and calling it's functions.


The functions encryptData and DecryptData are for encryption and decryption of a string message.
There is the function generateRandomKey for creating a random key for the algotithm,
but you can also test with your key.
All the other functions,are gliches to support the implementation of the algorithm.

It works for 16,24 and 32-bit Primary keys and for four mode of operations:
ECB,CBC,CFB and OFB.

**EXAMPLE OF USAGE: 

--In file (the one which will use it) 'myScript.py'-- 

import AES 

key = AES.generateRandomKey(16); 

                16 is the primary key size.It could be also 24 or 32. 

msn = AES.encryptData(key,"my message",'CFB'); 

                We encrypt the text "my message" with CFB mop.
                This function returns three values:
                1 the mode of operation used
                2 the encrypted message
                3 the iv for some of the modes required.
                
msn2 = AES.decryptData(msn[1],msn[0],key,msn[2]);
