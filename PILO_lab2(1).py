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
    
def isSimple(expr):     # элементарность функции перехода 
    simb = ['0','1','a','b','c','d']
    if expr in simb:
        return True
    else:
        return False


def skip(s, i):         # пропуск скобок
    ch = 1
    while (i < len(s)) and (ch!=0):
        if s[i] == '(':
            ch+=1
        elif s[i] == ')':
            ch-=1
        i+=1        
    return i-1


def brackets(s):        # удаление скобок снаружи для дальнейшего разбора
    if (s[0] == '(') and (s[len(s)-1] == ')'):
        return s[1:len(s)-1]
    else:
        return s
    
def refreshBeginEnd(graf, listBE):                  # на вход поступает список begins или ends
    for lett in listBE:                             # списки обновляются в соотвествии с преобразованиями графа
        isInGraf = False                            # н-р, после того, как удалены висячие и недостижимые вершины,
        i = 0                                       # их также нужно удалить из этих двух списков
        while (i < len(graf)) and (isInGraf == False):
            if (graf[i][0] == lett) or (graf[i][1] == lett):
                isInGraf = True
            i+=1
        if isInGraf == False:
            listBE.remove(lett)
    return listBE
    

def orf():              # разбор по ИЛИ
    temp=[]
    global graf, numb
    p1, p2 = 0, -2
    i=0
    
    graf[numb][2] = brackets(graf[numb][2])        # отбрасываем внешние скобки
    s = graf[numb][2]
    
    while i<(len(s)):
        if s[i] == '(':         # не трогаем внутренности внутренних скобок
            i = skip(s, i+1)-1
        elif (p2 != -2) and (i == len(s)-1):    # если знак | был раньше, но пришел конец строки,
            p1 = p2+2                           #  то копируем от | до конца
            p2 = len(s)-1
            temp.append(s[p1:p2+1])
        elif s[i] == '|':                      # копируем с начала до | 
            p1 = p2+2                          # или от | до |
            p2 = i-1
            temp.append(s[p1:p2+1])
        i+=1
    for j in range(len(temp)):
        struct = [graf[numb][0], graf[numb][1], temp[j], isSimple(temp[j])]  # добавляем в граф элементы, разветвленные по ИЛИ
        graf.insert(numb+1+j, struct)
    if len(temp)>0:                         # если разветвления были, то
        graf.pop(numb)                      # удаляем текущее 
        numb+=len(temp)-1                   # и сдвгаем numb на кол-во добавленных 
        return True
    else:
        return False
    

def andf():             # разбор по И
    global count, graf, numb
    simb = '01abc'
    was = False                 # были ли И в этом вызове функции
    noMult = False              # на текущей итерации нет И
    while (noMult == False):
        noMult = True
        i=0
        s = graf[numb][2]        
        while i<(len(s)-1):
            if s[i] == '(':         # пропускаем внутеренности скобок
                i = skip(s, i+1)-1
            elif (s[i] in simb+'*+)') and (s[i+1] in simb+'('):     # увидели комбинацию, которая есть И
                struct = [lett[count], graf[numb][1], s[i+1:], isSimple(s[i+1:])] # все что после И в новый элемент (с начальной новой буквой)
                graf.insert(numb+1,struct)
                graf[numb] = [graf[numb][0], lett[count], s[:i+1], isSimple(s[:i+1])]     # все что до И меняем в текущем элементе (с конечной новой буквой)
                count+=1            # для того чтобы следующая добавленная буква была новой
                noMult = False
                was = True
                numb+=1             # сдвигаем numb всегда на 1
                break
            i+=1
    return was
    

def iterf():            # разбор итераций
    global count, graf, numb
    s = graf[numb][2]
    if s[-1] == '+' or s[-1] == '*':        # + и * могут стоять только на последнем месте
        struct = [lett[count], graf[numb][1], 'e', True]                            # вторая дуга для всех по e
        graf.insert(numb+1,struct)
        struct = [lett[count], lett[count], s[:len(s)-1], isSimple(s[:len(s)-1])]               # кольцевая дуга по функции для всех
        graf.insert(numb+1,struct)                
        if s[-1] == '+':
            graf[numb] = [graf[numb][0], lett[count], s[:len(s)-1], isSimple(s[:len(s)-1])] # перва дуга по функции для +
        else:
            graf[numb] = [graf[numb][0], lett[count], 'e', True]                            # первая дуга по е для *
        count+=1            # новая буква
        numb+=2             # две новые связи
        return True
    else:
        return False
    
    
def diagram():                                  # функция строим диаграмму состояний по графу (по сути убирает е-дуги)
    global graf, count
    noE = False                                 # флаг "e-дуг больше нет" (изначально False)
    pointS = -1         
    while noE == False:
        noE = True
        i = 0
        epoints = []        # вершины пути от первой найденной е-дуги последней
        esycle = []         # вершины пути цикла по e-дугам
        while i < len(graf):
            if graf[i][2] == 'e':   # если нашли е-дугу
                noE = False
                pointS = i          # запоминаем связь, с которой все началось
                pointZ = i          # текущая найденная связь (станет последней)
                epoints.append(graf[i][0])
                break
            i+=1
        while i < len(graf):
            if (graf[i][0] == graf[pointZ][1]) and (graf[i][2] == 'e'):     # если нашли продолжение е-дуги от текущей связи
                pointZ = i                                                  # то меняем текущую связь на эту
                epoints.append(graf[i][0])
                if graf[i][1] in epoints:                                   # если такая вершина уже была, то это цикл
                    esycle = epoints[epoints.index(graf[i][1]):]
                    break 
            i+=1
            
        if noE == False:                        # если е-дуги были
            if graf[pointZ][1] in epoints:      # если нашелся цикл по е-дугам
                for j in esycle:                # то делаем из всего цикла одно обобщающее состояние
                    if j in begins:             # если были среди них начальные, то обобщающее состояние главное 
                        begins.append(esycle[0])
                    if j in ends:               # если были конечные, то обобщающее тоже конечное
                        ends.append(esycle[0])
                        
                i = 0
                while i < len(graf):            # заменяем все названия вершин цикла на одно общее
                    if graf[i][0] in esycle:
                        graf[i][0] = esycle[0]
                    if graf[i][1] in esycle:
                        graf[i][1] = esycle[0]
                    
                    i+=1
                
                i = 0
                while i < len(graf):            # появившиеся бесполезные состояния типа "из А в А по е" удаляем
                    if (graf[i][0] == esycle[0]) and (graf[i][1] == esycle[0]) and (graf[i][2] == 'e'):
                        graf.pop(i)
                        i-=1
                    i+=1
                        
            else:                                   # если цикла е-дуг не было
                if graf[pointS][0] in begins:       # делаем последнее состояние начальнм, если цепь е идет от начального
                    begins.append(graf[pointZ][1])
                if graf[pointZ][1] in ends:         # если уперлись в конечное, то предпоследнее становится тоже конечным
                    ends.append(graf[pointZ][0])    
                kol=0                               # количество дуг, исходивших из последнего состояния в е-цепи
                i=0
                while i < len(graf):    
                    if graf[i][0] == graf[pointZ][1]:       # если из последнего состояния что-то выходит, дублируем эти связи для предпоследнего
                        kol+=1
                        struct = [graf[pointZ][0], graf[i][1], graf[i][2], graf[i][3]]
                        graf.insert(i-1+kol, struct)
                        i+=1
                    i+=1
                graf.pop(pointZ)        # удаляем последнюю связь с е-дугой

    if pointS != -1:                    # если хоть раз е-дуга была найдена, то удаляем недостижимые состояния           
        i = 0
        while i < len(graf):
            if graf[i][0] not in begins:    # если оно не начальное и при этом из него что-то выходит,
                pastFree = True
                j=0
                while (j < len(graf)) and (pastFree == True):
                    if graf[j][1] == graf[i][0]:        
                        pastFree = False
                    j+=1
                if pastFree == True:        # но никто в него не ведет 
                    graf.pop(i)             # то удаляем такую связь
                    i-=1                   
            i+=1
            
def NKA (graf):
    nka = []
    numb = -1
    graf.sort()                 # сортируем граф по названию вершин для удобства
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
    print(nka)
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
    #nka = [['A', 'AB', 'C', False, True], ['B', '', 'C', True, True], ['C', '', 'AC', True, False]]
    #begins = ['A','B']
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

struct = ['from', 'to', 'expr', False] # структура элемента графа. last - isSimple
lett = list('QWERTYUIOPADFGHJKLXCVBNM')
lett.sort()
count=0             # порядковый номер добавляемого состояния (для lett(count++))

print('Enter a string: ')
S = input()

begins = ['S']               # множество начальных состояний
ends = ['Z']                 # множество конечных состояний
graf = []                                   # начинаем строить граф
struct = ['S', 'Z', S, isSimple(S)]   # добавляем первый элемент в граф (из S по введенной функции в Z)
graf.append(struct)


AllSimple = False

while (AllSimple == False):         # пока все функции переходов не танут элементарными
    AllSimple = True
    
    numb = 0
    while numb < len(graf):
        #if orf():                   # разбираем каждую функцию графа по ИЛИ
        #    print(graf)
        orf()
        numb+=1
    
    numb = 0
    while numb < len(graf):
        #if andf():                  # разбираем каждую функцию графа по ИЛИ
        #    print(graf)
        andf()
        numb+=1
        
    numb = 0
    while numb<len(graf):
        #if iterf():                 # разбираем каждую функцию по циклам
        #    print(graf)
        iterf()
        numb+=1      

    for k in range(len(graf)):    
        AllSimple = AllSimple and graf[k][3]        # логически перемножаем поля isSimple элементов графа

printGraf(graf)
diagram()
begins = refreshBeginEnd(graf, begins)
ends = refreshBeginEnd(graf, ends)
printGraf(graf)
nka = NKA(graf)
printTable(nka)
dka = DKA(nka)
printTable(dka)