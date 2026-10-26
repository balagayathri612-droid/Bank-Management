import json 
import random
import string 
from pathlib import Path 


class Bank:
    database = 'data.json'
    data = [] #holds dummy data of JSON file
    
    try:
        if Path(database).exists():
            with open(database) as fs:
                #loads data from json file and convert it into python object
                data = json.loads(fs.read())
        else:
            print("no such file exist ")
    except Exception as err:
        print(f"an exception occured as {err}")
    #private class method to update the data in the json file
    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters,k = 3)
        num = random.choices(string.digits,k= 3)
        spchar = random.choices("!@#$%^&*",k = 1)
        id = alpha + num + spchar
        random.shuffle(id) #after shuffle it vl be a list so we need to convert it into string
        return "".join(id)



    def Createaccount(self):
        info = {
            "name": input("Tell your name :- "),
            "age" : int(input("tell your age :- ")),
            "email": input("tell your email :- "),
            "pin": int(input("tell your 4 number pin :- ")),
            "accountNo." : Bank.__accountgenerate(),
            "balance" : 0
        }
        #converting the pin into string to check the length of it
        if info['age'] < 18  or len(str(info['pin'])) != 4:
            print("sorry you cannot create your account")
        else:
            print("account has been created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("please note down your account number")

            Bank.data.append(info)

            Bank.__update()
        
    def depositmoney(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))
#extracting the user data from the list of dictionary using list comprehension
#which will return user data user ccount no nd pin matches the given input datas
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
#empty dict vl give False so checking
        if userdata == False:
            print("soory no data found")
        
        else:
            amount = int(input("how much you want to depoit "))
            if amount  > 10000 or amount < 0:
                print("sorry the amount is too much you can deposit below 10000 and above 0")

            else:
                #userdata is a list of dictionary so we need to access the first element of it
                #and then access the balance key and add the amount to it
                userdata[0]['balance'] += amount
                Bank.__update()#updating JSON
                print("Amount deposited successfully ")
    

    def withdrawmoney(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))
    #list comprehension--> result : list of dic
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("soory no data found")
        
        else:
            amount = int(input("how much you want to withdraw "))
            if userdata[0]['balance']  < amount:
                print("soory you dont have that much money")
              
            else:
                
                userdata[0]['balance'] -= amount
                Bank.__update()
                print("Amount withdrew successfully ")


    def showdetails(self):

        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        print("your information are \n\n\n")
        #iterating through list of the keys of the dictionary and printing the key and value
        for i in userdata[0]: #i is key, value is userdata[0][i]
            print(f"{i} : {userdata[0][i]}")



    def updatedetails(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("no such user found ")
        
        else:
            print("you cannot change the age, account number, balance")

            print("Fill the details for change or leave it empty if no change")
#creating dummy data to store values from user
            newdata = {
                "name": input("please tell new name or press enter : "),
                "email":input("please tell your new Email or press enter to skip :"),
                "pin": input("enter new Pin or press enter to skip: ")
            }
#empty vl update old data
            if newdata["name"] == "":
                newdata["name"] = userdata[0]['name']
            if newdata["email"] == "":
                newdata["email"] = userdata[0]['email']
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]['pin']
   #non updatable datas         
            newdata['age'] = userdata[0]['age']

            newdata['accountNo.'] = userdata[0]['accountNo.']
            newdata['balance'] = userdata[0]['balance']
      #new data of pin is converted into int from str    
            if type(newdata['pin']) == str:
                newdata['pin'] = int(newdata['pin'])
            

            for i in newdata:
                 if newdata[i] == userdata[0][i]:
                     continue
                 else:
                     userdata[0][i] = newdata[i]

            Bank.__update()
            print("details updated successfully")


    def Delete(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("sorry no such data exist ")
        else:
            check = input("press y if you actually want to delete the account or press n")
            if check == 'n' or check == "N":
                print("bypassed")
            else:
                #getting index of account to be deteled
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("account deleted successfully ")
                #to update JSON from dummy data
                Bank.__update()

            

user = Bank()
print("press 1 for creating an account")
print("press 2 for Deposititing the money in the bank ")
print("press 3 for withdrawing the money ")
print("press 4 for details ")
print("press 5 for updating the details")
print("press 6 for deleting your account")

check = int(input("tell your response :- "))

if check == 1:
    user.Createaccount()

if check == 2:
    user.depositmoney()

if check == 3:
    user.withdrawmoney()

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()

if check == 6:
    user.Delete()