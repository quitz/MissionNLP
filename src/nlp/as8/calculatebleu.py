from __future__ import division
from collections import Counter
import sys
from itertools import izip
import math

# [685, 331, 194, 116] [1225, 1175, 1125, 1075]


def ngrams(input_line, n):
    input_line = input_line.split()
    if len(input_line) < n:
        input_line += (n - len(input_line) ) * ["-"]
        return []
        
    output = []
    for i in range(len(input_line)-n+1):
        output.append(input_line[i:i+n])
    
    return ["-".join(x) for x in output]

def calc_pn_value(candidate_line, reference_lines, gramCount):
    # max count of a word in any ref_counts 
    max_ref_counts = {}
    # count of nGrams in candidate
    candidate_ctr = Counter(ngrams(candidate_line, gramCount))
#     print candidate_ctr
    for reference_line in reference_lines:
        # count of nGrams in one reference translation
        ref_ctr = Counter(ngrams(reference_line, gramCount))
#         print ref_ctr
        for word in candidate_ctr:
            max_ref_counts[word] = max(ref_ctr[word] ,max_ref_counts.get(word, 0)) 
    
#     print max_ref_counts
    count_clipped = [min(count, max_ref_counts[word]) for word, count in candidate_ctr.items()]
#     print count_clipped

    return sum(count_clipped) , sum(candidate_ctr.values())

def calc_bp(candidate_line, reference_lines):

    c = len(candidate_line)
#     print c
    r = [len(reference_line) for reference_line in reference_lines]

    min_r = [abs(r_i - c) for r_i in r]
    r = r[min_r.index(min(min_r))]
#     print r
    
    # as per paper
    if c > r:
        return 1
    else:
        return math.exp(1 - r / c)



def strip_line(line):
    return line.strip("\n").strip()

def main_fn():
    # Take input dir
    candidate_data = sys.argv[1]
    ref_data = sys.argv[2]
    
    # if ref_data is file
    num = [0,0,0,0]
    denom = [0,0,0,0]
    bp = 0
    tot_x = [] 
    tot_y = [] 
    with open(candidate_data) as cand_file, open(ref_data) as ref_file: 
        for x, y in izip(cand_file, ref_file):
            #calculate Pn
            for i in range(1,5):
                pn_num, pn_den = calc_pn_value(strip_line(x), [strip_line(y)], i)
                num[i-1] += pn_num
                denom[i-1] += pn_den
            
            tot_x += strip_line(x) 
            tot_y += strip_line(y)
        
        # calculate bp for whole file    
        bp = calc_bp(tot_x, tot_y)
        
        ref_file.close()
        cand_file.close()
    
    print num, denom, bp
    score = 0
    for i in range(0,4):
        # TODO handle 0 error
        score += (0.25 * math.log(num[i] / denom[i]) )
    
    
    total_score = bp * math.exp(score)
    
    print total_score 
    
    with open("bleu_out.txt", "w") as fo:
        fo.write("{0}".format(total_score))     
    print "Whole file written"
        
print __name__
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main_fn() 



#     with open(candidate_data) as c_file, open(ref_data) as r_file:
#         tot_x = [] 
#         tot_y = [] 
#         for x, y in izip(c_file, r_file): 
#             tot_x += x.strip().split(" ") 
#             tot_y += y.strip().split(" ")
#         
#         print tot_x
#         print "---", bleu(tot_x, [tot_y], [0.25,0.25,0.25,0.25]) 
#         r_file.close()
#         c_file.close()