from pathlib import Path
import os
def createfile():
      try:
        name=input("enter your file name ")
        path=Path(name)
        if path.exists():
                print("this filename is already exists")
                print("write a file name which doesnt exists")
                createfile()
        else:
                file=open(path,"x")
                print("your file is created successfully")
                file.close()
      except Exception as err:
            print(f"error is occured {err}")
            
def writefile():
        try:
            name=input("enter your file name ")
            path=Path(name)
            if path.exists():
                file=open(path,"w")
                data=input("enter your data")
                file.write(data)
                file.close()
            else:
                print("wait your file creation is on process")
                file=open(path,"w")
                data=input("enter your data what you want to write!")
                file.write(data)
                file.close()
        except Exception as err:
            print(f"error is occured {err}")

def readfile():
        try:
            name=input("enter your file  name from which u want to fetch data")
            path=Path(name)
            if path.exists():
                file=open(path,"r")
                print(file.read())
                file.close()
            else:
                print("file is not found ")
                print("please retry")
                readfile()
        except Exception as err:
             print(f"error is occured {err}")

def updatefile():
        try:
            print("operations")
            print("1. renaming the file")
            print("2. add the content") 
            print("3. overwritting the file")
            choice=int(input("enter ur choice"))
            if choice==1:
                 name=input("enter file name for upadation")
                 path=Path(name)
                 newname=input("enter a new file name:- ")
                 newpath=Path(newname)
                 if newpath.exists():
                      print("this file name is already exists")
                 else:
                      path.rename(newpath)
                      print("updated sucessfully")

            elif choice==2:
                 name=input("enter a file name")
                 path=Path(name)
                 if path.exists():
                      with open(path,"a") as file :
                           data=input("enter data you want to add")
                           file.write(data)
                 else:
                      print("file doesn't exists")
            elif choice==3:
                 name=input("enter file name")
                 path=Path(name)
                 if path.exists():
                      with open(path, "w")as file:
                           data=input("enter data what u want to enter and overwrite your file")
                           file.write(data)
                 else:
                      print("file doesn't exists")
        except Exception as err:
             print(f"error is occured {err}")


def deletefile():
      try:
        name=input("enter your file name which you wnat to delete")
        path=Path(name)
        if path.exists():
            path.unlink()
            print("file deleted sucessfully")
        else: 
            print("file doesn't exists")
      except Exception as err:
           print(f"error occured {err}")


print("press 1 for creating a file")
print("press 2 for writing a file")
print("press 3 for reading a file")
print("press 4 for updateing a  file")
print("press 5 for deleting a file")


choice=int(input("enter your choice"))

if choice==1:
    createfile()
elif choice==2:
    writefile()
elif choice==3:
    readfile()
elif choice==4:
    updatefile()
elif choice==5:
    deletefile()
else:
    raise ValueError ("entered number is invalid")
