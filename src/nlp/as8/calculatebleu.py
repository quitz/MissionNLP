from __future__ import division
from collections import Counter
import sys
from itertools import izip
import math
import os
from dircache import listdir

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
#     print sum(candidate_ctr.values())
#     print candidate_line
    return sum(count_clipped) , sum(candidate_ctr.values())

def calc_cr_bp(candidate_line, reference_lines):
    
    c = len(candidate_line)

    r = [len(reference_line) for reference_line in reference_lines]
    
    delta_r = [abs(r_i - c) for r_i in r]
    r = r[delta_r.index(min(delta_r))]
#     print  c,[len(reference_line) for reference_line in reference_lines],r
    return c,r
    
def calc_bp(c,r):
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
    
    ref_files = [0]
    if os.path.isfile(ref_data):
        ref_files[0] = open(ref_data,"r")
    else:
        if ref_data[-1:] !="/":
            ref_data+="/"
              
        ref_files = [0]*len(listdir(ref_data))
        for idx,fn in enumerate(listdir(ref_data)):
            ref_files[idx] = open(ref_data + fn, 'r')
            
    # if ref_data is file
    num = [0,0,0,0]
    denom = [0,0,0,0]
    tot_x = [] 
    tot_y = [[]] * len(ref_files)
    tot_c = 0
    tot_r = 0
    
    with open(candidate_data) as cand_file: 
        for x in izip(cand_file):
            x = strip_line(x[0])
            # read ref files
            y = [0] * len(ref_files)
            for idx, ref_file in enumerate(ref_files):
                y[idx] = strip_line(ref_file.readline())
                if(tot_y[idx]):
                    tot_y[idx]+=y[idx].split()
                else:
                    tot_y[idx]=y[idx].split()
            
            #calculate Pn    
            for i in range(1,5):
                pn_num, pn_den = calc_pn_value(x, y, i)
                num[i-1] += pn_num
                denom[i-1] += pn_den
            
            tot_x += x.split()
            c,r= calc_cr_bp(x.split(), [yi.split() for yi in y])
            tot_c+=c
            tot_r+=r 
            
        # calculate bp for whole file    
        bp = calc_bp(tot_c, tot_r)
        
        for idx, ref_file in enumerate(ref_files):
            ref_file.close()
        cand_file.close()
    
    print num, denom, bp
    score = 0
    for i in range(0,4):
        # TODO handle 0 error
        if num[i] != 0 and denom[i] != 0:
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
