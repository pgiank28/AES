import os;
import sys;
import math;

# Rijndael S-box
sbox =  [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16];

# Rijndael Inverted S-box
rsbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
            0x9e, 0x81, 0xf3, 0xd7, 0xfb , 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
            0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb , 0x54,
            0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
            0x42, 0xfa, 0xc3, 0x4e , 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
            0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 , 0x72, 0xf8,
            0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
            0x65, 0xb6, 0x92 , 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
            0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 , 0x90, 0xd8, 0xab,
            0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
            0x45, 0x06 , 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
            0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b , 0x3a, 0x91, 0x11, 0x41,
            0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
            0x73 , 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
            0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e , 0x47, 0xf1, 0x1a, 0x71, 0x1d,
            0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b ,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
            0xfe, 0x78, 0xcd, 0x5a, 0xf4 , 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
            0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f , 0x60,
            0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
            0x93, 0xc9, 0x9c, 0xef , 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
            0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 , 0x17, 0x2b,
            0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
            0x21, 0x0c, 0x7d];

def getSBoxValue(num):
	"""Look-up function to sbox"""
	return sbox[num];

def getSBoxInvert(num):
	"""Look-up function to the inverted sbox"""
	return rsbox[num];

def rotate(word):
	""" Rijndael's key schedule rotate operation."""
	return word[1:] + word[:1];

# Rijndael Rcon
Rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
            0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97,
            0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72,
            0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66,
            0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
            0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
            0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
            0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61,
            0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
            0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
            0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc,
            0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
            0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
            0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
            0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c,
            0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
            0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4,
            0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
            0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08,
            0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
            0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
            0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2,
            0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74,
            0xe8, 0xcb ];

def getRconValue(num):
	"""Look-up function to rcon"""
	return Rcon[num];

def convertString(string, start, end,mode):
        if end - start > 16: end = start + 16;
	if modeOfOperation(mode)==3: 
		ar = [0] * 16;
        else: 
		ar = [];
        

        i = start
        j = 0
        while len(ar) < end - start:
            ar.append(0)
        while i < end:
	    if(type(string[i])==int):
		ar[j]=string[i];
            else:
		ar[j] = ord(string[i])
            j += 1
            i += 1
        return ar;


'''Stage 1 of the round'''
def addRoundKey(state, roundKey):
        """Adds (XORs) the round key to the state."""
        for i in range(16):
		if(type(roundKey[i])==int):
            		state[i] ^= roundKey[i];
		else:
			state[i] ^= ord(roundKey[i]);
        return state;

def createRoundKey(expandedKey, roundKeyPointer):
        """Create a round key.
        Creates a round key from the given expanded key and the
        position within the expanded key.
        """
        roundKey = [0] * 16;
        for i in range(4):
            for j in range(4):
                roundKey[j*4+i] = expandedKey[roundKeyPointer + i*4 + j];
        return roundKey;


'''Stage 2 of the round'''
def subBytes(state, isInv):
        if isInv: getter = getSBoxInvert;
        else: getter = getSBoxValue;
        for i in range(16): 
		state[i] = getter(state[i]);
        return state;


'''Stage 3 of the round'''
def shiftRows(state, isInv):
        for i in range(4):
            state = shiftRow(state, i*4, i, isInv);
        return state;

def shiftRow(state, statePointer, nbr, isInv):
        for i in range(nbr):
		if isInv:
			state[statePointer:statePointer+4] = \
				state[statePointer+3:statePointer+4] + \
				state[statePointer:statePointer+3];
		else:
			state[statePointer:statePointer+4] = \
				state[statePointer+1:statePointer+4] + \
				state[statePointer:statePointer+1];
        return state;



'''Stage 4 of the round'''
def galois_multiplication(a, b):
        """Galois multiplication of 8 bit characters a and b."""
        p = 0;
        for counter in range(8):
		if b & 1: p ^= a;
		hi_bit_set = a & 0x80;
		a <<= 1;
            # keep a 8 bit
		a &= 0xFF;
		if hi_bit_set:
			a ^= 0x1b;
		b >>= 1
        return p;

def mixColumns(state, isInv):
        # iterate over the 4 columns
        for i in range(4):
            # construct one column by slicing over the 4 rows
		column = state[i:i+16:4];
            # apply the mixColumn on one column
		column = mixColumn(column, isInv);
            # put the values back into the state
		state[i:i+16:4] = column;

        return state;

def mixColumn(column, isInv):
        if isInv: mult = [14, 9, 13, 11];
        else: mult = [2, 1, 1, 3];
        cpy = list(column);
        g = galois_multiplication;

        column[0] = g(cpy[0], mult[0]) ^ g(cpy[3], mult[1]) ^ \
                    g(cpy[2], mult[2]) ^ g(cpy[1], mult[3]);
        column[1] = g(cpy[1], mult[0]) ^ g(cpy[0], mult[1]) ^ \
                    g(cpy[3], mult[2]) ^ g(cpy[2], mult[3]);
        column[2] = g(cpy[2], mult[0]) ^ g(cpy[1], mult[1]) ^ \
                    g(cpy[0], mult[2]) ^ g(cpy[3], mult[3]);
        column[3] = g(cpy[3], mult[0]) ^ g(cpy[2], mult[1]) ^ \
                    g(cpy[1], mult[2]) ^ g(cpy[0], mult[3]);
        return column;

"""applies the 4 operations of the forward round in sequence"""
def aes_round(state, roundKey):
	state = subBytes(state, False);
	state = shiftRows(state, False);
	state = mixColumns(state, False);
	state = addRoundKey(state, roundKey);
	return state;

"""applies the 4 operations of the inverse round in sequence"""
def aes_invRound(state, roundKey):
	state = shiftRows(state, True);
        state = subBytes(state, True);
        state = addRoundKey(state, roundKey);
        state = mixColumns(state, True);
        return state;


"""The AES encryption algorithm"""
def encrypt(iput, key, size):
        output = [0] * 16

        # the number of rounds
        nbrRounds = 0

        # the 128 bit block to encode
        block = [0] * 16

        # set the number of rounds
        if size == 16: nbrRounds = 10
        elif size == 24: nbrRounds = 12
        elif size == 32: nbrRounds = 14
        else: return None

        # the expanded keySize
        expandedKeySize = 16*(nbrRounds+1)

	print "-Size of key = ",size,"\n-Size of expanded key = ",expandedKeySize,"\n";
        # Set the block values, for the block:
        # a0,0 a0,1 a0,2 a0,3
        # a1,0 a1,1 a1,2 a1,3
        # a2,0 a2,1 a2,2 a2,3
        # a3,0 a3,1 a3,2 a3,3
        # the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3
        #
        # iterate over the columns
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                block[(i+(j*4))] = iput[(i*4)+j]

        # expand the key into an 176, 208, 240 bytes key
        # the expanded key
        expandedKey = expandKey(key, size, expandedKeySize);

        # encrypt the block using the expandedKey
	state = addRoundKey(block, createRoundKey(expandedKey, 0));
        i = 1
        while i < nbrRounds:
		state = aes_round(state,createRoundKey(expandedKey, 16*i));
		i += 1;

	# The final round with no mixcolumns state
        state = subBytes(state, False)
        state = shiftRows(state, False)
        state = addRoundKey(state,createRoundKey(expandedKey, 16*nbrRounds));

        # unmap the block again into the serial output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k*4)+l] = state[(k+(l*4))];
        return output;


"""The AES decryption algorithm"""
def decrypt(iput, key, size):
        output = [0] * 16
        # the number of rounds
        nbrRounds = 0
        # the 128 bit block to decode
        block = [0] * 16
        # set the number of rounds
        if size == 16: nbrRounds = 10
        elif size == 24: nbrRounds = 12
        elif size == 32: nbrRounds = 14
        else: return None

        # the expanded keySize
        expandedKeySize = 16*(nbrRounds+1);

        # Set the block values, for the block:
        # a0,0 a0,1 a0,2 a0,3
        # a1,0 a1,1 a1,2 a1,3
        # a2,0 a2,1 a2,2 a2,3
        # a3,0 a3,1 a3,2 a3,3
        # the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3

        # iterate over the columns
	
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                block[(i+(j*4))] = iput[(i*4)+j];
        # expand the key into an 176, 208, 240 bytes key
        expandedKey = expandKey(key, size, expandedKeySize);
	
        # decrypt the block using the expandedKey
        state = addRoundKey(block,createRoundKey(expandedKey, 16*nbrRounds));
        i = nbrRounds - 1;
        while i > 0:
            state = aes_invRound(state,createRoundKey(expandedKey, 16*i));
            i -= 1;
        state = shiftRows(state, True)
        state = subBytes(state, True)
        state = addRoundKey(state, createRoundKey(expandedKey, 0));

	
        # unmap the block again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k*4)+l] = state[(k+(l*4))]
        return output

def encryptData(key, data, mode):
        # the AES input/output
        plaintext = [];
        iput = [0] * 16;
        output = [];
        ciphertext = [0] * 16;
	iv=[];
        # the output cipher array
        cipherOut = [];
	#The input key size
	size = len(key);
	
        # char firstRound
        firstRound = True;
	if data != None:
		
		if modeOfOperation(mode)== -1:
			print("Invalid mode of operation given.System aborted\n");
			return;

		if modeOfOperation(mode)==1:
			print "Starting encryption with :\n--ECB mode of operation\n--plaintext to be encrypted = ",data,"\n";
			for j in range(int(math.ceil(float(len(data))/16))):
				start=j*16;
				end=j*16+16;
				
				if  end > len(data):
                    			end = len(data);
				plaintext = convertString(data, start, end,mode);
				
				for i in range(end-start):
					iput[i]=plaintext[i];

				print "--",j," input to be encrypted after ECB operation = ",iput;
				ciphertext = encrypt(iput, key, size);
				for k in range(16):
                        		cipherOut.append(ciphertext[k]);
				
			print"--message after the AES encryption= ",cipherOut,"\n";

		elif modeOfOperation(mode)==2:
			
			print"Starting encryption with :\n--CBC mode of operation\n--plaintext to be encrypted = ",data,"\n";
			# create a new iv using random data
			iv = [ord(i) for i in os.urandom(16)];
			for j in range(int(math.ceil(float(len(data))/16))):
				start=j*16;
				end=j*16+16;
				
				if  end > len(data):
                    			end = len(data);
				plaintext = convertString(data, start, end,mode);
				for i in range(end-start):
					if firstRound:
						iput[i] =  plaintext[i] ^ iv[i];
					else:
						iput[i] =  plaintext[i] ^ ciphertext[i];
					
                    		print "--",j,"input to be encrypted after CBC operation = ",iput,"\n";
				firstRound = False;
				ciphertext = encrypt(iput, key, size);
				
                    	# always 16 bytes because of the padding for CBC
				for k in range(16):
					cipherOut.append(ciphertext[k]);
			
			print"--message after the AES encryption= ",cipherOut,"\n";

		elif modeOfOperation(mode)== 3:
			print "Starting encryption with :\n--CFB mode of operation\n--plaintext to be encrypted = ",data,"\n";
			# create a new iv using random data
			iv = [ord(i) for i in os.urandom(16)];
			for j in range(int(math.ceil(float(len(data))/16))):
                		start = j*16
                		end = j*16+16
                		if  end > len(data):
                    			end = len(data);
				
                		plaintext = convertString(data, start, end, mode)
                	# print 'PT@%s:%s' % (j, plaintext)
                		
                    		if firstRound:
                        		output = encrypt(iv, key, size);
                        		firstRound = False;
                    		else:
                        		output = encrypt(iput, key, size);

                    		for i in range(16):
                        		if len(plaintext)-1 < i:
                            			ciphertext[i] = 0 ^ output[i]
                        		elif len(output)-1 < i:
                            			ciphertext[i] = plaintext[i] ^ 0
                        		elif len(plaintext)-1 < i and len(output) < i:
                            			ciphertext[i] = 0 ^ 0
                        		else:
                            			ciphertext[i] = plaintext[i] ^ output[i]
                    		for k in range(end-start):
                        		cipherOut.append(ciphertext[k])

                   		iput = ciphertext
			print "--message after the AES encryption= ",cipherOut,"\n";

		elif modeOfOperation(mode)==4:
			print "Starting encryption with :\n--OFB mode of operation\n--data to be encrypted",data;
			# create a new iv using random data
			iv = [ord(i) for i in os.urandom(16)];
			for j in range(int(math.ceil(float(len(data))/16))):
				start = j*16
                		end = j*16+16
                		if  end > len(data):
                    			end = len(data)
                		plaintext = convertString(data, start, end, mode);
				if firstRound:
					output = encrypt(iv, key, size);
					firstRound = False;
				else:
					output = encrypt(iput, key, size);
				for i in range(16):
					if len(plaintext)-1 < i:
						ciphertext[i] = 0 ^ output[i];
					elif len(output)-1 < i:
						ciphertext[i] = plaintext[i] ^ 0;
					elif len(plaintext)-1 < i and len(output) < i:
						ciphertext[i] = 0 ^ 0;
					else:
						ciphertext[i] = plaintext[i] ^ output[i];
				for k in range(end-start):
					cipherOut.append(ciphertext[k]);
				iput = output;
               

        return mode, cipherOut,iv;
	
	return;

def decryptData(data, mode, key,iv):
        # the AES input/output
        ciphertext = []
        iput = []
        output = []
        plaintext = [0] * 16;
      
	#The input key size
	size = len(key);
	
	# the output plain text character list
        chrOut = [0]*size;

	# char firstRound
        firstRound = True;
        if data != None:
		ciphertext = data;
		if modeOfOperation(mode)==-1:
			print("Invalid mode of operation given.System aborted\n");
			return;
		if modeOfOperation(mode)==1:
			print "\nStarting decryption with :\n--ECB mode of operation\n--data to be decrypted = ",data;
			for j in range(int(math.ceil(float(len(data))/16))):
                		start = j*16;
                		end = j*16+16;
                		if j*16+16 > len(data):
                    			end = len(data);
                		ciphertext = data[start:end];
				output=decrypt(ciphertext, key, size);
				print "--",j,"output after AES decryption = ",output,"\n";
				for i in range(16):
					chrOut.append(output[i]);

			print "--final output after ECB operation = ",chrOut;

		elif modeOfOperation(mode)==2:
			print "Starting decryption with :\n--CBC mode of operation\n--data to be decrypted = ",data,"\n";
			originalsize=len(data);
			for j in range(int(math.ceil(float(len(data))/16))):
                		start = j*16;
                		end = j*16+16;
                		if j*16+16 > len(data):
                    			end = len(data);
                		ciphertext = data[start:end];
				output = decrypt(ciphertext, key, size);
				print "--",j,"output after AES decryption = ",output,"\n";

	                    	for i in range(end-start):
	                        	if firstRound:
                            			plaintext[i] = iv[i] ^ output[i];
                        		else:
                           			plaintext[i] = iput[i] ^ output[i];
                    		firstRound = False;
				iput=ciphertext;

                    		if originalsize is not None and originalsize < end:
                        		for k in range(originalsize-start):
                           			chrOut.append(chr(plaintext[k]));
				else:
                        		for k in range(end-start):
                        			chrOut.append(plaintext[k]);
				
                    	print "--final output after CBC operation = ",chrOut,"\n";

                elif modeOfOperation(mode)==3:
			print "Starting decryption with :\n--CFB mode of operation\n--data to be decrypted = ",data,"\n";
			
			
			for j in range(int(math.ceil(float(len(data))/16))):
                		start = j*16;
                		end = j*16+16;
                		if j*16+16 > len(data):
                    			end = len(data);
                		ciphertext = data[start:end];
 				if firstRound:
                        		output = encrypt(iv, key, size)
                        		firstRound = False
                    		else:
                        		output = encrypt(iput, key, size)

                    		for i in range(16):
                        		if len(output)-1 < i:
                            			plaintext[i] = 0 ^ ciphertext[i]
                        		elif len(ciphertext)-1 < i:
                            			plaintext[i] = output[i] ^ 0
                        		elif len(output)-1 < i and len(ciphertext) < i:
                            			plaintext[i] = 0 ^ 0
                        		else:
                            			plaintext[i] = output[i] ^ ciphertext[i]
                   		for k in range(end-start):
                        		chrOut.append(plaintext[k])
                    		iput = ciphertext

			print "--final output after CFB operation = ",chrOut,"\n";

                elif modeOfOperation(mode)==4:
			print "Starting decryption with :\n--OFB mode of operation\n--data to be decrypted ",data;
			
			for j in range(int(math.ceil(float(len(data))/16))):
                		start = j*16
                		end = j*16+16
                		if j*16+16 > len(data):
                    			end = len(data);
                		ciphertext = data[start:end]
                    		if firstRound:
                        		output = decrypt(iv, key, size);
                        		firstRound = False;
                    		else:
                        		output = decrypt(iput, key, size);
                    		for i in range(16):
                        		if len(output)-1 < i:
                            			plaintext[i] = 0 ^ ciphertext[i];
                        		elif len(ciphertext)-1 < i:
                            			plaintext[i] = output[i] ^ 0;
                        		elif len(output)-1 < i and len(ciphertext) < i:
                            			plaintext[i] = 0 ^ 0;
                        		else:
                            			plaintext[i] = output[i] ^ ciphertext[i];

                    		for k in range(end-start):
                        		chrOut.append(chr(plaintext[k]));
                    		iput = output;
               
        return chrOut;


def modeOfOperation(mode):
	'''Mode of operation codes'''
	'''Every mode is presented as an integer to the algorithm'''
	#ECB -> 1
	#CBC -> 2
	#CFB -> 3
	#OFB -> 4

	if(mode=="ECB"):
		return 1;
	if(mode=="CBC"):
		return 2;
	if(mode=="CFB"):
		return 3;
	if(mode=="OFB"):
		return 4;
	
	return -1;

def core( word, iteration):
        """Key schedule core for Rijndael's key expansion"""
        
        word = rotate(word);
        # apply S-Box substitution on all 4 parts of the 32-bit word
        for i in range(4):
		if(type(word[i]))==int:
			word[i] = getSBoxValue(word[i]);
		else:
			word[i] = getSBoxValue(ord(word[i]));

        # XOR the output of the rcon operation with i to the first part
        # (leftmost) only
        word[0] = word[0] ^ getRconValue(iteration)
        return word;

def expandKey(key, size, expandedKeySize):
        """Rijndael's key expansion."""
        
        currentSize = 0; # current expanded keySize, in bytes
        I = 1;  #the rcon counter
        expandedKey = [0] * expandedKeySize;

        # set the 16, 24, 32 bytes of the expanded key to the input key
        for j in range(size):
            expandedKey[j] = key[j];
        currentSize += size

        while currentSize < expandedKeySize:
            # assign the last 4 bytes to the temporary value t
            t = expandedKey[currentSize-4:currentSize];

            # every 16,24,32 bytes we apply the core schedule to t
            # and increment rconIteration afterwards
            if currentSize % size == 0:
                t = core(t, I);
                I += 1;

            # For 256-bit keys, we add an extra sbox to the calculation
            if size == 256 and ((currentSize % size) == 16):
                for l in range(4): 
			t[l] = getSBoxValue(t[l]);

            # We XOR t with the four-byte block 16,24,32 bytes before the new
            # expanded key.  This becomes the next four bytes in the expanded
            # key.
            for m in range(4):
		if(type(expandedKey[currentSize - size])==int):
			expandedKey[currentSize] = expandedKey[currentSize - size] ^ \
                        t[m];
		else:
                	expandedKey[currentSize] = ord(expandedKey[currentSize - size]) ^ \
                        t[m];
                currentSize += 1

        return expandedKey;


def generateRandomKey(keysize):
    """Generates a key from random data of length `keysize`.    
    The returned key is a string of bytes.    
    """
    if keysize not in (16, 24, 32):
        emsg = 'Invalid keysize, %s. Must be one of (16, 24, 32).'
        raise ValueError, emsg % keysize
    return os.urandom(keysize);




