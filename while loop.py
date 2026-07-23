#i=9

#while i>0:
#    print(i)
 #   i-=2


 #i=0
#while i<10:
#    print(i)
#    i+=2

#password=""
#while password!="python":
 #   password=(input("enter password:"))

#print("Access granted")

balance=5000
while True:

    print("/n =====ATM MENU====")
    print("1.deosit")
    print("2.withdraw")
    print("3.balance check")
    print("Exit")

    choice=int(input("Enter your choice:"))
    if choice==1:
        amount=int(input("Enter deposit amount:"))

        if amount>0:
            balance=balance+amount
            print("Amount deposited successfully")
            print("current balance:",balance)
        else:
            print("deposit amount must be positive")

    elif choice==2:
        amount=int(input("enter withdraw amount:"))
        if amount<=balance:
            balance=balance-amount
            print("Amount withdraw successfull")
        else:
            print("insufficient amount")
        print("current balance:",balance)
    

    elif choice==3:
        print("your available balance is:",balance)
    elif choice==4:
        print("Thank u for using ATM")
        break
    else:
        print("invalid choice")
