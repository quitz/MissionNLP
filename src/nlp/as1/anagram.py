#Prints all permutations of a string
import sys

res = []
def perm(start, remain):
    if(len(remain) == 0):
        res.append(start)
        
    for i in range(len(remain)):
        perm(start + remain[i], ''.join(remain[:i] + remain[i + 1:]))
         

#Take input word
ipWord = sys.argv[1]
print "Input - {0}\n".format(ipWord) 

perm('', ipWord)
res.sort()

sorted_op = ''
for w in res:
    sorted_op += w + '\n'

with open('anagram_out.txt', 'w') as f:
    f.write(sorted_op)
    f.close()

print 'stored result in anagram_out.txt'

        
