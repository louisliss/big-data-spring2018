#A.1 create a list containing any four strings
list_one = ['hello','i','am','list']
print(list_one)

#A.2 print the third item in the list
print(list_one[2])

#A.3 print the 1st and 2nd item in the list using [:] index slicing.
print(list_one[0:2])

#A.4 Add a new string with text “last” to the end of the list and print the list.
list_one.append('Last')
print(list_one)

#A.5 Get the list length and print it.
print(len(list_one))

#A.6 Replace the last item in the list with the string “new” and print
del list_one[len(list_one)-1]
list_one.append('new')
print(list_one)

#B.1 Convert the list into a normal sentence with join(), then print.
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
s = " "
print(s.join(sentence_words))

#B.2 Reverse the order of this list using the .reverse() method, then print. Your output should begin with [“them”, ”visualize”, … ].
sentence_words.reverse()
print(sentence_words)

#B.3 Now user the .sort() method to sort the list using the default sort order.
sentence_words.sort()
print(sentence_words)

#B.4 Perform the same operation using the sorted() function. Provide a brief description of how the sorted() function differs from the .sort() method.
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
print(sorted(sentence_words))
print(sentence_words)
#Looks like both .sort and sorted() put the list in case-sensitive alphabetical order.
#However, .sort saves the sorted order into the original list, while sorted() does not save the new order.

#B.5 Extra Credit: Modify the sort to do a case case-insensitive alphabetical sort.
#Thank you, Matthias Eisen
sentence_words_alph = sorted(sentence_words, key = lambda x: x.lower())
print(sentence_words_alph)

#C Random function
from random import randint
greetings = "Welcome to the random integer generator!"
print(greetings)
upper = int(input("Enter an upper bound integer: "))
lower = int(input("Enter a lower bound integer, or hit enter for 0: ") or "0")
# this returns random integer: 100 <= number <= 1000
num = randint(lower, upper)
print(num)
'''not sure what's up with the assert function
assert(lower <= num <= upper)'''

#D Sting Formatting function
title = str(input("Please input bestseller title")).title()
print(title)
n = int(input("Please input bestseller's rank"))
sentence = f'The number {n} bestseller today is {title}'
print(sentence)

#E Password validation function
#thank you Zhubarb on stackexchange for your code

import re
password = str(input("Input a password to test: "))
uc = re.search(r"[A-Z]", password)
print(uc)
if uc = True



def hasnumbers(password):
    ''' Check whether the input string is a digit. '''
    try:
        int(s)
        return True
    except:
        # do not catch error
        return False
def check_validity(pw):
    ''' Return True if input pw is valid, and return False if invalid.'''
    special_chars = ['$','#','@']
    if isinstance(pw,str): pw=list(pw) # I could have appointed to a diff var name
    else: warnings.warn('Password has to be a string object.')
    res = False
    valid_dict={'small_let':False, 'num':False, 'special_chars':False,
                'cap_let':False, 'len':False } # is using a dict efficient?
    if len(pw)>= 6: valid_dict['len']=True
    for i in pw:
        if i.islower(): valid_dict['small_let'] = True
        if i in special_chars: valid_dict['special_chars'] = True
        if i.isupper(): valid_dict['cap_let'] = True
        if not valid_dict['num']:  valid_dict['num'] = check_number(i)
    if all(valid_dict.values()): res = True
    return res

print(check_validity(password))
