# Function is a block of code that performs a specific task.
# it is defined using "def" keyword. 
# syntax: 
#     def function_name():
#        code

'''
def fun():
    print("hello world") 
fun()
'''

'''
def add(a,b):
    print(a+b)
add(10,20) 
'''

'''name="sneha"
print(len(name))
'''

# Arbitrary arguments- how many arguments we have to pass is unknown
# keyword
# arbitrary keyword-don't know how many keywords are pass, then add '**'
# default
 
''' arbitrary
def func(*name):
    print(f"my name is {name[1]}")
func("sneha","harsha","shiva")
'''

# if we want to pass two arguments, arbitrary arguments are placed at last.otherwise it will take all values to single parameter.
# ex:
# def fun(age,*name)

''' Keyword
def func(a1,a2,a3):
    print(f"my name is {a3}")
func(a1="sneha",a2="harsha",a3="shiva")
'''

'''
def func(**child):
    print(f"my name is {child['kid']}")
func(kid="sneha",kid1="shiva",kid2="harsha")
'''

'''
def func(name,age=20,gender="female"):
    print(f"my name is {name}")
    print(f"i am {age}yrs old.")
    print(f"i am a {gender} gender")
func("sneha")
'''

# if i want to change age,gender i have to write in func.
# func("sneha",21,gender="male")

'''
def add(a,b):
    return a+b
print("sum=",add(10,20))
'''
 
# if variable declared inside a fun -local variable.
# if variable declared outside a fun -global variable

'''
a=10
def fun1():
    print(a)

def fun2():
    b=20
    print(a,b)
fun1()
fun2()
'''

# lamda fun is an anonymous function,
# that can take any no.of arguments but can contains only one expression and returns result automatically.
# syntax
# lambda arguments:expression

'''
add=lambda a, b :a+b
print(add(10,20))
'''

'''
square=lambda a:a*a
print(square(15))
'''

'''
large=lambda a,b:a if a>b else b
print(large(57,84))
'''

'''
num=[1,2,3,4]
result=list(map(lambda x:x*2,num))
#print(list(map(lambda x:x*2,num)))
print(result)
'''

num=[10,20,30,49,52,64,75]
#print(list(filter(lambda x:x%10==0,num)))
print(sorted(num,reverse=True))