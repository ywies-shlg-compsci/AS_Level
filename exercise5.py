text = input("enter a text")

if text[len(text)-3:] == "ing":
    text = [text,"ly"]
    newtext = ''.join(text)
else:
    text = [text, "ing"]
    newtext = ''.join(text)

print(newtext)
