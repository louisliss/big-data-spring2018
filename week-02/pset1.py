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
'''instructions = "Welcome to the random number generator. Please choose "
from random import randint
# this returns random integer: 100 <= number <= 1000
num = randint(100, 1000)

lower = input('Please input the lower bound: ')
