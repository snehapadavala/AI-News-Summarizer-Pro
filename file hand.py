'''used to create,read,write,update and delete files stored in computer-File Handling
data stored permenantly
opening file:
syntax
file_object=open("filename","mode")

modes:
1.read mode-used to read existing files
2.write mode-
   creates a file if it doesnt exist.
   delete old content
3.append mode-
   create file if it doesnot exist.
   add content without deletind existing data.
4.ceate mode(x)
creates a new file only.

read(size)- reads specific characters
readline()- reads one line(first line)
readlines()- returns  list.
writelines()- writes multiple lines

using with open()-automatically close file
syntax:
with open("file.txt","mode")as variable:
  operation
'''

'''f=open("hello.txt","r")
print(f.read())
f.close()
'''

'''f=open("hello.txt","a")
f.write("\nthis is datavally class")
f.close()
'''

# f=open("new.txt","x")

'''f=open("hello.txt","r")
print(f.read(10))
f.close()
'''

'''f=open("hello.txt","r")
print(f.readline())
print(f.readline())
f.close()
'''

'''
f=open("hello.txt","r")
lines=f.readlines()
print(lines[2])
'''

# f=open("hello.txt","r")
# print(f.readlines())

'''
f=open("new.txt","w")
data=["A\n","B\n","c"]
f.writelines(data)
'''

with open("hello.txt","r")as f:
    print(f.read())

with open("hello.txt","a")as b:
    b.write("\n python fullstack")  