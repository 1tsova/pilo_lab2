def isSimple(expr):     # �������������� ������� �������� 
    if (expr == '0') or (expr == '1'):
        return True
    else:
        return False


def skip(s, i):         # ������� ������
    ch = 1
    while (i < len(s)) and (ch!=0):
        if s[i] == '(':
            ch+=1
        elif s[i] == ')':
            ch-=1
        i+=1        
    return i-1


def brackets(s):        # �������� ������ ������� ��� ����������� �������
    if (s[0] == '(') and (s[len(s)-1] == ')'):
        return s[1:len(s)-1]
    else:
        return s
    

def orf():              # ������ �� ���
    temp=[]
    global graf, numb
    p1, p2 = 0, -2
    i=0
    
    graf[numb][2] = brackets(graf[numb][2])        # ����������� ������� ������
    s = graf[numb][2]
    
    while i<(len(s)):
        if s[i] == '(':         # �� ������� ������������ ���������� ������
            i = skip(s, i+1)-1
        elif (p2 != -2) and (i == len(s)-1):    # ���� ���� | ��� ������, �� ������ ����� ������,
            p1 = p2+2                           #  �� �������� �� | �� �����
            p2 = len(s)-1
            temp.append(s[p1:p2+1])
        elif s[i] == '|':                      # �������� � ������ �� | 
            p1 = p2+2                          # ��� �� | �� |
            p2 = i-1
            temp.append(s[p1:p2+1])
        i+=1
    for j in range(len(temp)):
        struct = [graf[numb][0], graf[numb][1], temp[j], isSimple(temp[j]), graf[numb][4]]  # ��������� � ���� ��������, ������������� �� ���
        graf.insert(numb+1+j, struct)
    if len(temp)>0:                         # ���� ������������ ����, ��
        graf.pop(numb)                      # ������� ������� 
        numb+=len(temp)-1                   # � ������� numb �� ���-�� ����������� 
        return True
    else:
        return False
    

def andf():             # ������ �� �
    global count, graf, numb
    simb = '01'
    was = False                 # ���� �� � � ���� ������ �������
    noMult = False              # �� ������� �������� ��� �
    while (noMult == False):
        noMult = True
        i=0
        s = graf[numb][2]        
        while i<(len(s)-1):
            if s[i] == '(':         # ���������� ������������� ������
                i = skip(s, i+1)-1
            elif (s[i] in simb+'*+)') and (s[i+1] in simb+'('):     # ������� ����������, ������� ���� �
                struct = [lett[count], graf[numb][1], s[i+1:], isSimple(s[i+1:]), graf[numb][4]] # ��� ��� ����� � � ����� ������� (� ��������� ����� ������)
                graf.insert(numb+1,struct)
                graf[numb] = [graf[numb][0], lett[count], s[:i+1], isSimple(s[:i+1]), False]     # ��� ��� �� � ������ � ������� �������� (� �������� ����� ������)
                count+=1            # ��� ���� ����� ��������� ����������� ����� ���� �����
                noMult = False
                was = True
                numb+=1             # �������� numb ������ �� 1
                break
            i+=1
    return was
    

def iterf():            # ������ ��������
    global count, graf, numb
    s = graf[numb][2]
    if s[-1] == '+' or s[-1] == '*':        # + � * ����� ������ ������ �� ��������� �����
        if s[-1] == '+':
            struct = [lett[count], graf[numb][1], s[:len(s)-1], isSimple(s[:len(s)-1]), graf[numb][4]] # ������ ���� �� ������� ��� +
        else:
            struct = [lett[count], graf[numb][1], 'e', True, graf[numb][4]]                            # ������ ���� ����� �� e ��� *
        graf.insert(numb+1,struct)
        struct = [lett[count], lett[count], s[:len(s)-1], isSimple(s[:len(s)-1]), False]               # ��������� ���� �� ������� ��� ����
        graf.insert(numb+1,struct)                
        graf[numb] = [graf[numb][0], lett[count], 'e', True, False]                                    # ����� ���� �� � ��� ����
        count+=1            # ����� �����
        numb+=2             # ��� ����� �����
        return True
    else:
        return False


struct = ['from', 'to', 'expr', False, True] # ��������� �������� �����. last two - isSimple, isEnd
lett = list('QWERTYUIOPADFGHJKLXCVBNM')
lett.sort()
count=0             # ���������� ����� ������������ ��������� (��� lett(count++))

print('Enter a string: ')
S = input()

graf = []
struct = ['S', 'Z', S, isSimple(S), True]   # ��������� ������ ������� � ���� (�� S �� ��������� ������� � Z)
graf.append(struct)


AllSimple = False

while (AllSimple == False):         # ���� ��� ������� ��������� �� ����� �������������
    AllSimple = True
    
    numb = 0
    while numb < len(graf):
        if orf():                   # ��������� ������ ������� ����� �� ���
            print(graf)
        numb+=1
    
    numb = 0
    while numb < len(graf):
        if andf():                  # ��������� ������ ������� ����� �� ���
            print(graf)
        numb+=1
        
    numb = 0
    while numb<len(graf):
        if iterf():                 # ��������� ������ ������� �� ������
            print(graf)
        numb+=1      

    for k in range(len(graf)):    
        AllSimple = AllSimple and graf[k][3]        # ��������� ����������� ���� isSimple ��������� �����
