"""The letter Algorithm - Arabic text Decryption (Steganography)"""
__version__ = "1.0.3"
__description__ ="The letter Algorithm - Arabic text Decryption (Steganography)"

import arabic_reshaper as ar
from os import system

class database:
    def __init__(self):
        self.DB={
        "ا":1, "ب":2, "ج":3,"د":4,"ه":5,"و":6,"ز":7,"ح":8,"ط":9,
        "ي":10,"ك":20,"ل":30,"م":40,"ن":50,"س":60,"ع":70,"ف":80,"ص":90,
        "ق":100,"ر":200,"ش":300,"ت":400,"ث":500,"خ":600,"ذ":700,"ض":800,"ظ":900,
        "غ":1000,"ء":1,"ؤ":1,"ى":1,"ة":400,"ئ":1,"أ":1
        }
        
    def get_value(self,letter):
        return self.DB.get(letter)

    def get_letter(self,number):
        for k,v in self.DB.items():
            if v==number:
                return k
    
    def get(self):
        return self.DB

class spliter:
    def __init__(self,values):
        self.VALUES=values

    def splite(self,slice):
        return [self.VALUES[x:x+slice] for x in range(0, len(self.VALUES), slice)]
           
    def hash_splite(self,slice):
        i =len(self.VALUES)-1
        splited=[]
        while i>=0:
            curr_lst=[]
            for _ in range(slice):
                if i<0:
                    break
                curr_lst.append(self.VALUES[i])
                i-=1
            splited.append(curr_lst)
            
        return splited

    



class arabic:
    def __init__(self, txt,codepage=None):
        if codepage != None:
            codepage()
        self.NTEXT=txt
        self.TEXT=self.reshape(txt)
    
    def reshape(self , txt):
        reshaped = ar.reshape(txt)
        return reshaped[::-1]

    def new(self,txt):
        self.TEXT=self.reshape(txt)

    def draw(self):
        print(self.TEXT)

    def size(self):
        return len(self.NTEXT)

    def get(self):
        return self.TEXT

    def getn(self):
        return self.NTEXT

    def values(self):
        db =database()
        vals = []
        i = self.size()-1
        while i>=0:
            if self.NTEXT[i]!=' ':
                val = db.get_value(self.NTEXT[i])
                vals.append(val)    
            i-=1
        return vals

    def hash_list(self,vals):
        hashval=[]
        for i in range(len(vals)):
            hashval+=str(vals[i])
        return hashval

    def hash_str(self,vals):
        hashval=""
        for i in range(len(vals)):
            hashval+=str(vals[i])
        return hashval


def applyPattren(hashstr,wordSize):
    i=len(hashstr)-1
    finalWord=[]
    while i>=0:
        sevlst=[]
        for _ in range(wordSize):
            if i<0:
                break
            if hashstr[i]=='6' and hashstr[i+1]!='0':
                onelst=[] 
                onelst.append(hashstr[i])
                finalWord.append(onelst)
                i-=1
                break
            else:
                sevlst.append(hashstr[i])
            i-=1

        if len(sevlst)>0:
            finalWord.append(sevlst)
        
    return finalWord
          
          
          
def getResponse(txtList, wordSize):
    response=""
    db =database()
    for l in txtList:
        tmp=l[::-1]
        #print(tmp)
        if len(tmp)==wordSize:
            i=wordSize-1
            while i>=0:
                #1
                
                if tmp[i]=='0' and tmp[i-1]!='0' and i-1>0:
                    nm=int(tmp[i-1]+'0')
                    response+=db.get_letter(nm)
                    #print(tmp[i-1]+'0')
                    i-=2
                #2
                elif tmp[i]=='0' and tmp[i-1]=='0' and tmp[i-2]!='0':
                    nm=int(tmp[i-2]+'00')
                    response+=db.get_letter(nm)
                    #print(tmp[i-2]+'00')
                    i-=3
                #3
                elif tmp[i]!='0' and tmp[i-1]=='0' and tmp[i-2]!='0':
                    nm=int(tmp[i])
                    response+=db.get_letter(nm)
                    #print(tmp[i])
                    i-=2
                #4
                elif tmp[i]!='0' and tmp[i-1]!='0':
                    nm=int(tmp[i])
                    nm1=int(tmp[i-1]+"0")
                    response+=db.get_letter(nm)
                    response+=db.get_letter(nm1)
                    #print(tmp[i])
                    #print(tmp[i-1]+"0")
                    i-=2
                #5
                elif tmp[i]=='0' and i-1<0:
                    i-=1
                    break
                #6
                elif tmp[i]=='0' and i-1==0 and tmp[i-1]!='0':
                    nm=int(tmp[i-1]+'0')
                    response+=db.get_letter(nm)
                    i-=1
                    #break   
                else:
                    if int(tmp[i-1])>int(tmp[i]):
                        nm=int(tmp[i])
                        nm1=int(tmp[i-1]+'0')
                        response+=db.get_letter(nm)
                        response+=db.get_letter(nm1)

                        #print(tmp[i])
                        #print(tmp[i-1]+'0')
                        i-=2
                    else:
                        #7  
                        nm=int(tmp[i])
                        res=db.get_letter(nm)
                        if res != None:
                             #print(tmp[i])
                             response+=res
                        i-=1
        
        elif len(tmp)==1:
            nm=int(tmp[0])
            response+=db.get_letter(nm)
            #print(tmp[0])
        else:
            return freeResponse(txtList)
        response+=" "
    return response
    


def freeResponse(txtList):
    response=""
    db =database()
    for l in txtList:
        tmp=l[::-1]
        #print(tmp)
        i=len(tmp)-1
        if len(tmp)-1==1:
            nm=int(tmp[0]) 
            response+=db.get_letter(nm)
            response+=" "

        while i>=0:
            #1
            if tmp[i]=='0' and tmp[i-1]!='0' and i-1>0:
                nm=int(tmp[i-1]+'0')
                response+=db.get_letter(nm)
                #print(tmp[i-1]+'0')
                i-=2
            #2
            elif tmp[i]=='0' and tmp[i-1]=='0' and tmp[i-2]!='0':
                nm=int(tmp[i-2]+'00')
                response+=db.get_letter(nm)
                #print(tmp[i-2]+'00')
                i-=3
            #3
            elif tmp[i]!='0' and tmp[i-1]=='0' and tmp[i-2]!='0':
                nm=int(tmp[i])
                response+=db.get_letter(nm)
                #print(tmp[i])
                i-=2
            #4
            elif tmp[i]!='0' and tmp[i-1]!='0':
                nm=int(tmp[i])
                nm1=int(tmp[i-1]+"0")
                response+=db.get_letter(nm)
                response+=db.get_letter(nm1)
                #print(tmp[i])
                #print(tmp[i-1]+"0")
                i-=2
            #5
            elif tmp[i]=='0' and i-1<=0:
                i-=1
                break
            #6   
            else:
                if int(tmp[i-1])>int(tmp[i]):
                    nm=int(tmp[i])
                    nm1=int(tmp[i-1]+'0')
                    response+=db.get_letter(nm)
                    response+=db.get_letter(nm1)

                    #print(tmp[i])
                    #print(tmp[i-1]+'0')
                    i-=2
                else:
                    #7 
                    nm=int(tmp[i])
                    response+=db.get_letter(nm)
                    #print(tmp[i])
                    i-=1
        response+=" "
    return response           
        
            
def text_process(hashstr):
    i= len(hashstr)-1
    finalText=""
    db = database()
    while i>=0:
        if hashstr[i]=='0' and hashstr[i-1]!='0' and hashstr[i-2] !='0':
            acharat = int(hashstr[i-1]+'0')
            miat = int(hashstr[i-2]+'00')
            achl = db.get_letter(acharat)
            miatl=db.get_letter(miat)
            finalText+=achl
            finalText+=miatl
            i-=3
        elif hashstr[i]!='0' and hashstr[i-1]=="0" and hashstr[i-2]!="0":
            ahad = int(hashstr[i])
            ahadl = db.get_letter(ahad)
            finalText+=ahadl
            acharat= int(hashstr[i-2]+"0")
            acharatl=db.get_letter(acharat)
            finalText+=acharatl
            i-=3
        elif hashstr[i]=='0' and hashstr[i-1]!="0":
            ach = int(hashstr[i-1]+"0")
            achl = db.get_letter(ach)
            finalText+=achl
            i-=2
        else:
            if hashstr[i] !='0':
                l = int(hashstr[i])
                ll = db.get_letter(l)
                if ll != None:
                    finalText+=ll
                #print("else ", hashstr[i])
            i-=1
    
    return finalText


def arabiCodePage():
    system("chcp 1256")


def test():
    arabiCodePage()
    while True:
        try:
            ques = arabic(input("#"))
            print("input:")
            ques.draw()
            
            print("out:")
            vals = ques.values()
            print(vals)
            vals_hash = ques.hash_str(vals)
            print(vals_hash)
            finalList = applyPattren(vals_hash,7)
            #try1
            response = getResponse(finalList,4)
            arResponse=arabic(response)
            arResponse.draw()
            #try2
            response = getResponse(finalList,7)
            arResponse=arabic(response)
            arResponse.draw()
            #other pattren
            anotherlst = applyPattren(vals_hash,5)
            for i in anotherlst:
                tmp=""
                for j in range(len(i)):
                    tmp+=i[j]
                anotherRes=text_process(tmp)
                anotherResAr = arabic(anotherRes)
                anotherResAr.draw() 
        except:
            pass

test()



        





