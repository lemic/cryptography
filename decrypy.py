import numpy as np


def main():
    cfile = open('ctext.txt','r')
    pfile = open('ptext.txt','w')
    ctext = "".join(line.strip() for line in cfile)  #remove whitespace, join lines from cfile
    N = determinekeylength(ctext)
    validkeys = determinekeys(ctext, N)
    cfile.close()
    pfile.close()

    
def determinekeylength(ctext):
    print ('Determining key length...')
    keylenrange = range(1,13)
    maxsumqisquared=0
    for keylen in keylenrange:
        i=0
        hexcharcount = [0]*256  # initialise list of hex character count
        while i <len(ctext):
            hexcharcount[int(ctext[i:i+2],16)]+=1
            i+=keylen
        q=[x/sum(hexcharcount) for x in hexcharcount]   
        sumqisquared=sum([qi**2 for qi in q])    
        print ('Sum of qi squared for key length of ', keylen, ': ', sumqisquared)
        if sumqisquared>maxsumqisquared:
            N=keylen
            maxsumqisquared=sumqisquared
    print ('Key length = ', N)  
    return N


def determinekeys(ctext, N):
    validkeys = [0]*N
    maxsumqp=[0]*N     
    p=[0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,0.02015,
        0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,0.06749,
        0.07507,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,
        0.00978,0.02360,0.00150,0.01974,0.00074]
    for n in range(1,N):
        print ('Solving key #', n, '...') 
        for key in range(0,255):
            print ('Trying key=',key, ' (in decimal)')
            lowerlettercount= [0]*26
            i=0+(n-1)*2
            invalidkey=False
            while i<len(ctext):
                decryptedchar=key^int(ctext[i:i+2],16)
                if (decryptedchar<32 or decryptedchar>127):
                    print ('Non printable character found.')
                    #print ('Encrypted character (in hex)=', ctext[i:i+2])
                    #print ('Decrypted character(in decimal)=', decryptedchar)
                    print ('Key=', key, ' is invalid.')
                    invalidkey=True
                    break
                elif (decryptedchar>47 and decryptedchar<58):
                    print ('Number found.')
                    #print ('Encrypted character (in hex)=', ctext[i:i+2])
                    #print ('Decrypted character(in decimal)=', decryptedchar)
                    print ('Key=', key, ' is invalid.')
                    invalidkey=True
                    break
                elif (decryptedchar>96 and decryptedchar<123):
                    lowerlettercount[decryptedchar-97]+=1
                    i+=N
            if not invalidkey:
                q = [x/sum(lowerlettercount) for x in lowerlettercount]
                sumqp = np.inner(p,q)
                if sumqp>maxsumqp:
                    maxsumqp[n-1] = sumqp
                    validkeys[n-1] = key
    print ('Valid keys: ', validkeys)
    print ('Sum of qi*pi for each key: ', maxsumqp)
    
if __name__ == "__main__":
    main()
