import numpy as np
headerInfo="wpi"
kvals="j5a0edj2b"
mVal=6
#initialize the dictionary
print("--------- initializing dictionary ---------")
mapin=dict({'a':0})
currchar=97   
for x in range(26):
    mapin[chr(currchar)]=format(x,"05b")
    mapin[format(x,"05b")]=chr(currchar)
    currchar+=1
currchar=48
for x in range(6):
    mapin[chr(currchar)]=format(x+26,"05b")
    mapin[format(x+26,"05b")]=chr(currchar)
    currchar+=1
print(mapin)
print("------------- dictionary made -------------")
#end dictionary initialization

#init header and crypt to bin
trueHead=""
for i in headerInfo:
    trueHead = trueHead+mapin[i]
trueK=""
#init k
for i in kvals:
    trueK=trueK+mapin[i]
#print initialization vector
IV = [mVal]
IV = [0]*(mVal)
svals=[0]*(2*mVal)
print("Initialization vector: ",end="")
for i in range(len(svals)):
    svals[i]=(int(trueK[i])+int(trueHead[i]))%2
    if i < mVal:
        print(svals[i], end="")
#print curr key
print("\nk is currently : "+trueK)
kk = [mVal]
kk=[0]*(mVal)
#print what we need to solve
for i in range(6,len(svals)):
    print(i)
    kk[(i-6)]=svals[i]

rows,cols=(mVal,mVal)
#get our matrix
matrix= [[svals[abs(x+y-1)] for x in range(cols,0,-1)] for y in range(mVal)]#[[0 for x in range(mVal+1)] for y in range(mVal+1)]
#solve the matrix for taps
smidvals=np.ndarray.tolist(np.linalg.solve(matrix,kk).astype(int))
#print our taps
print("feedback vals: "+str(smidvals))
dec=""
#decrypt and print it.
for x in range(len(trueK)):
    hold=0
    dec=dec + str(((int(svals[mVal-1])+int(trueK[x]))%2))

    for y in range(mVal):
        if (smidvals[y]%2) ==1:
            hold+=svals[y]
    hold=hold%2
    for y in range(mVal-1,0,-1):
        svals[y]=svals[y-1]

    svals[0]=hold
idk=[dec[i:i+5] for i in range(0, len(dec), 5)]

decryptStr=""
for x in range(len(idk)):
    decryptStr+=mapin.get(idk[x])
print("decrypted: "+ str(decryptStr))
