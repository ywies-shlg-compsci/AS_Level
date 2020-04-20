string = input("enter a text")

if len(string) < 2:
    print(" ")
elif len(string) == 2:
    string = [string,string]
    newstring = ''.join(string)
    print(newstring)
elif len(string) > 2:
    string = [string[:2],string[-2:]]
    newstring = ''.join(string)
    print(newstring)
