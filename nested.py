'''
for i in range(1,4):
    for j in range(2,5):
        print(i,j)
       print(i,j,end=" ")
       '''

'''
for i in range(5):
    for j in range(i+1):
        print("*",end=" ")
    print()
    '''


'''
for i in range(5):
    for j in range(i):
       print("*",end=" ")
    print()
'''

# @@@@@@@@@@@BREAK@@@@@@@@@@@
#for i in range(1,10):
#    if i==5:
#        break
#    print(i)

#i=1
##    print(i)
#    i+=1
#    if i==5:
#        break

#for i in range(5):
#    if i==3:
#        continue
#    print(i)

#continue will skip one iteration

'''
i=0
while i<10:
    i+=1
    if i%2==0:
        continue
    print(i)
    '''
# pass gives nothing.

for i in range(1,6):
    print("*" * i+" "*(2*(6-i))+"*" *i)

for i in range(5,0,-1):
    print("*" * i +" "*(2*(6-i))+"*" *i)