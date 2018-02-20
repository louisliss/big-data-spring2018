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

def rfunc(upper, lower = 0):
    upper = int(input("Enter an upper bound integer: "))
    lower = int(input("Enter a lower bound integer, or hit enter for 0: ") or "0")
    return randint(lower,upper)

print(rfunc(lower,upper))

assert(100 <= rfunc(100,1000) <= 1000)

#D Sting Formatting function
title = str(input("Please input bestseller title")).title()
print(title)
n = int(input("Please input bestseller's rank"))
sentence = f'The number {n} bestseller today is {title}'
print(sentence)

#E Password validation function
# adapted from https://codereview.stackexchange.com/questions/135634/password-validator-using-regular-expressions/135663

password = str(input("Input a password to test: "))

def checklength(password):
    if 8 > len(password) or 14 < len(password)  :
        return False
    else:
        return True

def checkdigits(password):
    if sum(c.isdigit() for c in password) < 2 :
        return False
    else:
        return True

def checkuppercase(password):
    if sum(c.isupper() for c in password) < 1 :
        return False
    else:
        return True

def checkspecial(password):
    special = ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    if any(c in password for c in special) :
        return True
    else:
        return False

def validate(password):
    if checklength(password) is False :
        return "Password must be between 8 and 14 characters"
    elif checkdigits(password) is False :
        return "Password must have at least one digit"
    elif checkuppercase(password) is False :
        return "Password must have at least one uppercase letter"
    elif checkspecial(password) is False :
        return "Password must have at least one special character !?@#$%^&*()-_+="
    else:
        return "Password is valid!"

print(validate(password))

#F Exponentiation function
# Malik Brahimi you're a champ https://stackoverflow.com/questions/30414784/recursive-power-function-step


a = int(input("What number would you like to exponentiate? "))
n = int(input("To which power would you like to raise your number? "))

def exponentiate (a,n):
    if n == 0 :
        return 1
    elif n == 1:
        return a
    else:
        return a * exponentiate(a, n-1)

print(exponentiate(a,n))

#G.1 Min function

l = input("Type in a list of numbers separated by a space: ")
numbers = list(map(int, l.split( )))
numbers.sort()

def minim(numbers):
    for x in numbers:
        if x > x+1 :
            return x+1
        else:
            return x

print(minim(numbers))

#G.2 Max function


l = input("Type in a list of numbers separated by a space: ")
numbers = list(map(int, l.split( )))
numbers.sort(reverse = True)

def maxim(numbers):
    for x in numbers:
        if x < x+1 :
            return x
        else:
            return x+1

print(maxim(numbers))
