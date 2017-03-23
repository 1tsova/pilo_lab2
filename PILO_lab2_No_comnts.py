def printGraf(graf):
    print('from\tto\thow\tbegin\tend')
    for i in range(len(graf)):
        print(graf[i][0], graf[i][1], graf[i][2], int(graf[i][0] in begins), int(graf[i][1] in ends), sep = '\t')
    print()
    
def printTable(nka):
    print('begin\t \t0\t1\tend')
    for i in (nka):
        print(i[-1], i[0], i[1], i[2], i[3], sep = '\t')

def isSimple(expr):     
    simb = ['0','1','a','b','c','d']
    if expr in simb:
        return True
    else:
        return False


def skip(s, i):         
    ch = 1
    while (i < len(s)) and (ch!=0):
        if s[i] == '(':
            ch+=1
        elif s[i] == ')':
            ch-=1
        i+=1        
    return i-1


def brackets(s):        
    if (s[0] == '(') and (s[len(s)-1] == ')'):
        return s[1:len(s)-1]
    else:
        return s
    
def refreshBeginEnd(graf, listBE):                  
    for lett in listBE:                             
        isInGraf = False                            
        i = 0                                       
        while (i < len(graf)) and (isInGraf == False):
            if (graf[i][0] == lett) or (graf[i][1] == lett):
                isInGraf = True
            i+=1
        if isInGraf == False:
            listBE.remove(lett)
    return listBE
    

def orf():              
    temp=[]
    global graf, numb
    p1, p2 = 0, -2
    i=0
    
    graf[numb][2] = brackets(graf[numb][2])        
    s = graf[numb][2]
    
    while i<(len(s)):
        if s[i] == '(':         
            i = skip(s, i+1)-1
        elif (p2 != -2) and (i == len(s)-1):    
            p1 = p2+2                           
            p2 = len(s)-1
            temp.append(s[p1:p2+1])
        elif s[i] == '|':                      
            p1 = p2+2                          
            p2 = i-1
            temp.append(s[p1:p2+1])
        i+=1
    for j in range(len(temp)):
        struct = [graf[numb][0], graf[numb][1], temp[j], isSimple(temp[j])]  
        graf.insert(numb+1+j, struct)
    if len(temp)>0:                         
        graf.pop(numb)                      
        numb+=len(temp)-1                   
        return True
    else:
        return False
    

def andf():             
    global count, graf, numb
    simb = '01abc'
    was = False                 
    noMult = False              
    while (noMult == False):
        noMult = True
        i=0
        s = graf[numb][2]        
        while i<(len(s)-1):
            if s[i] == '(':         
                i = skip(s, i+1)-1
            elif (s[i] in simb+'*+)') and (s[i+1] in simb+'('):     
                struct = [lett[count], graf[numb][1], s[i+1:], isSimple(s[i+1:])] 
                graf.insert(numb+1,struct)
                graf[numb] = [graf[numb][0], lett[count], s[:i+1], isSimple(s[:i+1])]     
                count+=1            
                noMult = False
                was = True
                numb+=1             
                break
            i+=1
    return was
    

def iterf():            
    global count, graf, numb
    s = graf[numb][2]
    if s[-1] == '+' or s[-1] == '*':        
        struct = [lett[count], graf[numb][1], 'e', True]                            
        graf.insert(numb+1,struct)
        struct = [lett[count], lett[count], s[:len(s)-1], isSimple(s[:len(s)-1])]               
        graf.insert(numb+1,struct)                
        if s[-1] == '+':
            graf[numb] = [graf[numb][0], lett[count], s[:len(s)-1], isSimple(s[:len(s)-1])] 
        else:
            graf[numb] = [graf[numb][0], lett[count], 'e', True]                            
        count+=1            
        numb+=2             
        return True
    else:
        return False
    
    
def diagram():                                  
    global graf, count
    noE = False                                 
    pointS = -1         
    while noE == False:
        noE = True
        i = 0
        epoints = []        
        esycle = []         
        while i < len(graf):
            if graf[i][2] == 'e':   
                noE = False
                pointS = i          
                pointZ = i          
                epoints.append(graf[i][0])
                break
            i+=1
        while i < len(graf):
            if (graf[i][0] == graf[pointZ][1]) and (graf[i][2] == 'e'):     
                pointZ = i                                                  
                epoints.append(graf[i][0])
                if graf[i][1] in epoints:                                   
                    esycle = epoints[epoints.index(graf[i][1]):]
                    break 
            i+=1
            
        if noE == False:                        
            if graf[pointZ][1] in epoints:      
                for j in esycle:                
                    if j in begins:             
                        begins.append(esycle[0])
                    if j in ends:               
                        ends.append(esycle[0])
                        
                i = 0
                while i < len(graf):            
                    if graf[i][0] in esycle:
                        graf[i][0] = esycle[0]
                    if graf[i][1] in esycle:
                        graf[i][1] = esycle[0]
                    
                    i+=1
                
                i = 0
                while i < len(graf):            
                    if (graf[i][0] == esycle[0]) and (graf[i][1] == esycle[0]) and (graf[i][2] == 'e'):
                        graf.pop(i)
                        i-=1
                    i+=1
                        
            else:                                   
                if graf[pointS][0] in begins:       
                    begins.append(graf[pointZ][1])
                if graf[pointZ][1] in ends:         
                    ends.append(graf[pointZ][0])    
                kol=0                               
                i=0
                while i < len(graf):    
                    if graf[i][0] == graf[pointZ][1]:       
                        kol+=1
                        struct = [graf[pointZ][0], graf[i][1], graf[i][2], graf[i][3]]
                        graf.insert(i-1+kol, struct)
                        i+=1
                    i+=1
                graf.pop(pointZ)        

    if pointS != -1:                    
        i = 0
        while i < len(graf):
            if graf[i][0] not in begins:    
                pastFree = True
                j=0
                while (j < len(graf)) and (pastFree == True):
                    if graf[j][1] == graf[i][0]:        
                        pastFree = False
                    j+=1
                if pastFree == True:        
                    graf.pop(i)             
                    i-=1                   
            i+=1
            
def NKA (graf):
    nka = []
    numb = -1
    graf.sort()                 
    curr = ''
    for i in range (len(graf)):
        if graf[i][0] != curr:
            numb += 1
            curr = graf[i][0]
            if graf[i][2] == '0':
                line = [curr, graf[i][1], '', curr in ends, curr in begins]
            elif graf[i][2] == '1':
                line = [curr, '', graf[i][1], curr in ends, curr in begins]
            nka.append(line)
        else:
            if graf[i][2] == '0':
                nka[numb][1] += graf[i][1]
            elif graf[i][2] == '1':            
                nka[numb][2] += graf[i][1]
    
    i = 0  
    while i < len(nka):
        if nka[i][4]:
            nka.insert(0, nka[i])
            nka.pop(i+1)
        i+=1
        
    i = 0    
    while i < len(nka):
        if (nka[i][3] == True) and (nka[i][4] == False): 
            nka.append(nka[i])
            nka.pop(i)
        else:
            i+=1
    
    return nka

struct = ['from', 'to', 'expr', False] 
lett = list('QWERTYUIOPADFGHJKLXCVBNM')
lett.sort()
count=0             

print('Enter a string: ')
S = input()

begins = ['S']               
ends = ['Z']                 
graf = []                                   
struct = ['S', 'Z', S, isSimple(S)]   
graf.append(struct)


AllSimple = False

while (AllSimple == False):         
    AllSimple = True
    
    numb = 0
    while numb < len(graf):
        
        
        orf()
        numb+=1
    
    numb = 0
    while numb < len(graf):
        
        
        andf()
        numb+=1
        
    numb = 0
    while numb<len(graf):
        
        
        iterf()
        numb+=1      

    for k in range(len(graf)):    
        AllSimple = AllSimple and graf[k][3]        

printGraf(graf)
diagram()
begins = refreshBeginEnd(graf, begins)
ends = refreshBeginEnd(graf, ends)
printGraf(graf)
nka = NKA(graf)
printTable(nka)