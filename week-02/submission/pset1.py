# A.1 create a list containing 4 strings
list1 = ['doing', 'big data homework', 'is', 'guess the word']
#A.2 print the third item in the list
print(list1[2])
#A.3 print the 1st and 2nd item in the list using [:] index slicing
print (list1[:2])
#A.4 add a new string to the end
list1.append('last')
print (list1)
#A.5 Get the list length and print it.
print(len(list1))
#A.6 Replace the last item in the list with the string “new” and print
list1[len(list1)-1]='new'
print(list1)


#B.STRINGS
#B.1 Convert the list into a normal sentence with join(), then print.
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
print(' '.join(sentence_words))
#B.2 Reverse the order of this list using the .reverse() method, then print. Your output should begin with [“them”, ”visualize”, … ].
sentence_words.reverse()
print(sentence_words)
#B.3 Sort the list using default sort order
sentence_words.sort()
print(sentence_words)
#B.4 sorted function
sentence_words_sorted= sorted(sentence_words)
print (sentence_words_sorted)
# the .sort() is a method which modifies the original list, while
# sorted() is a function which sorts the list without modifying the
#original one.


#B.5 modify the sort to do a case
sentence_words.sort(key=lambda s: s.lower())
print (sentence_words)
#default sequence of sort function: symbols, numeric, capital letter, lowercase letter (alphabetical order)

#C. random function
from random import randint
max=20
def ran_func(max, min=0):
    return randint(min,max)
assert(0<=ran_func(20,0)<=20)



#D string formatting function
n=1
book_title='Harry Potter and the philosophy Stone'
book_title.title()
print('The number {} bestseller today is: {}'.format(n, book_title))


#E.password validation function
password='nvU1ajfoan!'
def code_val(password):
    count_dig=0
    count_upp=0
    count_spe=0
    m=['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']

    import string

    if len(password)<=14 and len(password)>=8:
        cond1=True
    else:
        cond1=False

    for i in range(len(password)):
        if string.digits.find(password[i])!=-1:# i is a digit
            count_dig += 1
        if string.ascii_uppercase.find(password[i])!=-1:
            count_upp += 1
        if password[i] in m:
            count_spe += 1

    if count_dig>=2:
        cond2=True
    else:
        cond2=False

    if count_upp>=1:
        cond3=True

    if count_spe>=1:
        cond4= True

    if cond1 and cond2 and cond3 and cond4:
        return 'password sucessfully set'
    else:
        return 'password not validated'

print(code_val(password))

#F.Exponetiation function
def exp(a,b):
    output=1
    for i in range(b):
        output=output*a
    return output
print(exp(3,-1))

#G.min and max functions
list= [1,4,5,2,3,7,9]
def min(list):
    if len(list)<=1:
        return None
    else:
        lo=list[0]
        hi=list[1]
        if lo>hi:
            lo=list[1]
            hi=list[0]
        for i in range(2,len(list)):
            if list[i]<lo:
                hi=lo
                lo=list[i]
            elif list[i]>lo and list[i]<hi:
                hi=list[i]
        return lo

def max(list):
    if len(list)<=1:
        return None
    else:
        lo=list[0]
        hi=list[1]
        if lo>hi:
            lo=list[1]
            hi=list[0]
        for i in range(2,len(list)):
            if list[i]>hi:
                lo=hi
                hi=list[i]
            elif list[i]>lo and list[i]<hi:
                lo=list[i]
        return hi

print(max(list))
print(min(list))
