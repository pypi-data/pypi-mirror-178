def crop():
    input1=input("enter the word")
    input2=input("enter the word")
    g={'b':7,'a':4,'s':8,'e':3,'l':5,'g':1,'m':9}
    fl={7:'b',4:'a',8:'s',3:'e',5:'l',1:'g',9:'m'}
    l=[]
    p=[]
    for i in input1:
        k=(g.get(i))
        l.append(k)
    for i in input2:
        o=(g.get(i))
        p.append(o)
    sums=[]
    for i in range(len(l)):
        if len(l)==len(p):
            s=l[i]
            f=p[i]
            k=s+f
            sums.append(k)
    for i in sums[::-1]:
        if sums.index(i)==0:
            pass
        else:
            sk=str(i)
            if len(sk)==2:
                io=sums.index(i)
                sums[io]=int(sk[1])
                sums[io-1]=sums[io-1]+1
    play=sums
    final=[]
    for i in play:
        final.append(str(i))
    fop=tuple(final)
    hk=(''.join(fop))
    lok=[]
    for i in range(len(hk)):
        lok.append(int(hk[i]))
    jk=[]
    for i in lok:
        jk.append(fl.get(i))
    print(''.join(jk))
def cr():
    print('''input1=input("enter the word")
input2=input("enter the word")
g={'b':7,'a':4,'s':8,'e':3,'l':5,'g':1,'m':9}
fl={7:'b',4:'a',8:'s',3:'e',5:'l',1:'g',9:'m'}
l=[]
p=[]
for i in input1:
    k=(g.get(i))
    l.append(k)
for i in input2:
    o=(g.get(i))
    p.append(o)
sums=[]
for i in range(len(l)):
    if len(l)==len(p):
        s=l[i]
        f=p[i]
        k=s+f
        sums.append(k)
for i in sums[::-1]:
    if sums.index(i)==0:
        pass
    else:
        sk=str(i)
        if len(sk)==2:
             io=sums.index(i)
             sums[io]=int(sk[1])
             sums[io-1]=sums[io-1]+1
play=sums
final=[]
for i in play:
    final.append(str(i))
fop=tuple(final)
hk=(''.join(fop))
lok=[]
for i in range(len(hk)):
    lok.append(int(hk[i]))
jk=[]
for i in lok:
    jk.append(fl.get(i))
print(''.join(jk))''')
