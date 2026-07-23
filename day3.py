# list is mutable,allow duplicate values,maintain order of elements. '[]'
# store any type of data in list. ex:[1,2,'s','hello',3.4]
# operations:indexing,slicing,append,reverse,update
#
# indexing:positive(left to right,start with 0),negative(right to left,start with -1)
#slicing means extracting.contains (start:stop:step).
#in negative slicing we have to represent -1 at step place,otherwise it dons'nt give output
#
# reverse ->[::-1]

# tuple is immutable,maintain order. '()'
# in tuple we write elements without using paranthesis. ex: 1,3,2
# 
# we can repeate the tuple by using '*'.ex: print(a*3)
# 
#a=(1,3,2,4)
#b=list(a)
#print(b)

#while using dict function we use paranthesis and use =symbol. ex: a=dict(name="a",age=23).
#squares={x:x**2 for x in range(1,6)}
#print(squares)

a={"name":"sneha","age":19}
#a["city"]="pdrk"
#print(a.get("name"))

# pop method removes particular single values in dict.
# popitem deletes last element.
# 
a.clear()
print(a)
# clear methid deletes only elements in dict.it shows empty dict.
# del removes total dict