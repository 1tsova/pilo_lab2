def printGraf(graf):
    print('from\tto\thow\tbegin\tend')
    print('------------------------------------')
    for i in range(len(graf)):
        print(graf[i][0], graf[i][1], graf[i][2], '1' if graf[i][0] in begins else '', '1' if (graf[i][1] in ends) else '', sep = '\t')
    print()
    
def printTable(ka):
    print('begin\t \t0\t1\tend')
    print('------------------------------------')
    for i in (ka):
        print('->' if i[-1] else '', ''.join(i[0]), ''.join(i[1]), ''.join(i[2]), '1' if i[3] else '', sep = '\t')
    print()
    
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
        printGraf(graf)
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
    printGraf(graf)
def NKA (graf):
    nka = []
    numb = -1
    graf.sort()                 
    curr = ['']
    for i in range (len(graf)):
        if graf[i][0] != curr[0]:
            numb += 1
            curr[0] = graf[i][0]
            if graf[i][2] == '0':
                line = [curr[:], [graf[i][1]], [], curr[0] in ends, curr[0] in begins]
            elif graf[i][2] == '1':
                line = [curr[:], [], [graf[i][1]], curr[0] in ends, curr[0] in begins]
            nka.append(line)
        else:
            if graf[i][2] == '0':
                nka[numb][1].append(graf[i][1])
            elif graf[i][2] == '1':            
                nka[numb][2].append(graf[i][1])
    for lett in ends:
        isInNka = False        
        for j in range(len(nka)):
            if nka[j][0][0] == lett:
                isInNka = True
        if isInNka == False:
            nka.append([[lett], [], [], lett in ends, lett in begins])
    
    i = 0  
    while i < len(nka):
        if nka[i][4]:
            nka.insert(0, nka[i])
            nka.pop(i+1)
        i+=1

    kol = 0
    i = 0    
    while i < len(nka) - kol:
        if (nka[i][3] == True) and (nka[i][4] == False): 
            kol+=1
            nka.append(nka[i])
            nka.pop(i)
        else:
            i+=1
    
    return nka

def DKA(nka):
    
    
    begins.sort()
    dka = [[begins, [], [], False, False]]
    newPositions = [dka[0][0]]
    
    for lett in begins:
        for i in range (len(nka)):
            if nka[i][0][0] == lett:
                for l in range (len(nka[i][1])):
                    if nka[i][1][l] not in dka[0][1]:
                        dka[0][1].append(nka[i][1][l])
                for l in range (len(nka[i][2])):
                    if nka[i][2][l] not in dka[0][2]:
                        dka[0][2].append(nka[i][2][l])                
                dka[0][3] = dka[0][3] or nka[i][3]
                dka[0][4] = dka[0][3] or nka[i][4]
    dka[0][1].sort()
    dka[0][2].sort()
    i = 0
    while i < len(dka):
        for j in range (1,3):
            if dka[i][j] not in newPositions:
                newPositions.append(dka[i][j])
                line = [dka[i][j], [], [], False, False]
                for lett in (dka[i][j]):
                    for k in range (len(nka)):
                        if nka[k][0][0] == lett:
                            for l in range (len(nka[k][1])):
                                if nka[k][1][l] not in line[1]:
                                    line[1].append(nka[k][1][l])
                            for l in range (len(nka[k][2])):
                                if nka[k][2][l] not in line[2]:
                                    line[2].append(nka[k][2][l])                                
                            line[3] = line[3] or nka[k][3]
                            line[4] = line[4] or nka[k][4]
                dka.append(line)
                dka[-1][1].sort()
                dka[-1][2].sort()                
        i+=1
    
    return dka

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


graf = [['S', 'Z', '1', True], ['S', 'A', '0', True], ['A', 'D', 'e', True], ['D', 'D', '1', True], ['D', 'B', 'e', True], ['B', 'E', 'e', True], ['E', 'G', '1', True], ['G', 'E', '0', True], ['E', 'H', '0', True], ['H', 'H', '0', True], ['H', 'E', 'e', True], ['E', 'C', 'e', True], ['C', 'F', '1', True], ['F', 'F', '1', True], ['F', 'Z', 'e', True]]

printGraf(graf)
diagram()
begins = refreshBeginEnd(graf, begins)
ends = refreshBeginEnd(graf, ends)
printGraf(graf)
nka = NKA(graf)
printTable(nka)
dka = DKA(nka)
printTable(dka)