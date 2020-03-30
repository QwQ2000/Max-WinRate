import shelve

db = shelve.open('data',flag = 'r')
etc = db['etc']
cte = db['cte']
wrate = db['wrate']
anti = db['anti']
comb = db['comb']

picked = []

while 1:
    cmd = input()
    if cmd[0] == 'a':
        cmd = cmd.split(' ')[1:]
        cmd[1] = cte[cmd[1]]
        picked.append(cmd)
    elif cmd[0] == 'l':
        lst = []
        for k,v in wrate.items():
            r = v
            flag = 0
            for h in picked:
                if h[1] == k:
                    flag = 1
                    break
                if h[0] == '0':
                        r *= comb[k][h[1]] / v
                else:
                        r *= anti[k][h[1]] / v
            if flag:
                continue
            lst.append([k,r])
        for x in sorted(lst,key = lambda x:x[1],reverse = True):
            print('%7s\t%.2f%%' % (etc[x[0]],x[1] * 100))
    elif cmd[0] == 'e':
        exit()
    elif cmd[0] == 'p':
        print('我方：',end = '')
        for h in picked:
            if h[0] == '0':
                print(etc[h[1]],end = '  ')
        print('\n敌方：',end = '')
        for h in picked:
            if h[0] != '0':
                print(etc[h[1]],end = '  ')
        print('')    
        
db.close() 