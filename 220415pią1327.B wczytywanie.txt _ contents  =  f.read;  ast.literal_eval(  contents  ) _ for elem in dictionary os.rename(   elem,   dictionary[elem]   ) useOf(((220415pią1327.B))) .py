
f  =  open(   "220415pią141358 TheOnlyTime+GPS LOG NumOfRenamedPictures1 dictionary .txt"
            , "r"   )
print( f )


contents  =  f.read()


import ast
dictionary  =  ast.literal_eval(  contents  )


import os
for elem in dictionary:
    print(   f'\n\t\t\t\t   {  elem  }\n{  dictionary[ elem ]  }'   )
    os.rename(                 elem,       dictionary[ elem ]       )
