def printGraf(graf):
    print('откуда\tкуда\tпо чему')
    for i in range(len(graf)):
        print(graf[i][0], '\t', graf[i][1], '\t', graf[i][2])
                
def isSimple(expr):     # элементарность функции перехода 
    if (expr == '0') or (expr == '1'):
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
    simb = '01'
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
        if s[-1] == '+':
            struct = [lett[count], graf[numb][1], s[:len(s)-1], isSimple(s[:len(s)-1])] # вторая дуга по функции для +
        else:
            struct = [lett[count], graf[numb][1], 'e', True]                            # вторая дуга также по e для *
        graf.insert(numb+1,struct)
        struct = [lett[count], lett[count], s[:len(s)-1], isSimple(s[:len(s)-1])]               # кольцевая дуга по функции для всех
        graf.insert(numb+1,struct)                
        graf[numb] = [graf[numb][0], lett[count], 'e', True]                            # перва дуга по е для всех
        count+=1            # новая буква
        numb+=2             # две новые связи
        return True
    else:
        return False
    
    
def diagram():
    global graf, count
    noE = False
    while noE == False:
        noE = True
        i = 0
        while i < len(graf):
            if graf[i][2] == 'e':
                noE = False
                pointS = i
                pointZ = i
                break
            i+=1
        while i < len(graf):
            if (graf[i][0] == graf[pointZ][1]) and (graf[i][2] == 'e'):
                pointZ = i
                if graf[pointZ][1] == graf[pointS][0]:
                    break #sycle
            i+=1
            
        if noE == False:
            if graf[pointS][0] in begins:
                begins.add(graf[pointZ][1])
            if graf[pointZ][1] in ends:
                ends.add(graf[pointZ][0])
            kol=0
            i=0
            while i < len(graf):
                if graf[i][0] == graf[pointZ][1]:
                    kol+=1
                    struct = [graf[pointZ][0], graf[i][1], graf[i][2], graf[i][3]]
                    graf.insert(i-1+kol, struct)
                    i+=1
                i+=1
            graf.pop(pointZ) # сначала добавить, потом pop        
        
    

struct = ['from', 'to', 'expr', False] # структура элемента графа. last - isSimple
lett = list('QWERTYUIOPADFGHJKLXCVBNM')
lett.sort()
count=0             # порядковый номер добавляемого состояния (для lett(count++))

print('Enter a string: ')
S = input()

begins = {'S'}               # множество начальных состояний
ends = {'Z'}                 # множество конечных состояний
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
print(begins, ends)
printGraf(graf)