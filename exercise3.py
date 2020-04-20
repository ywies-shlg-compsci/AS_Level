Str1 = "abc"
Str2 = "xyz"

String1 = [Str2[0:2],Str1[2:3]]
String2 = [Str1[0:2],Str2[2:3]]
Answer1 = ''.join(String1)
Answer2 = ''.join(String2)
NewString = [Answer1,Answer2]
Answer = ' '.join(NewString)

print(Answer)
