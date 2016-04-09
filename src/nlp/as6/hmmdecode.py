# Tag using hmmmodel generate from hmmlearn
'''
dictionary of words_to_tag_counts 
key -> word
value -> counter of tag_to_next_tag_count for this word
This will be used in emission probability
''' 

from __future__ import division
from math import log10
from collections import Counter
import sys
from hmmUtils import * 

NEG_INF = -sys.maxint - 1

words_to_tag_counts = {}

'''
dictionary of tag_to_next_tag_count 
key -> a tag i
value -> counter of tag_to_next_tag_count coming after tag i
This will be used in transition probability
''' 
tag_to_next_tag_count = {}

'''
counter of tag_to_next_tag_count
This will be used to count tag_to_next_tag_count
''' 
tag_counts = Counter()


def calculate_transition_prob(tag_word, prev_tag):
    '''
    calculate transition probability prev_tag, tag_word
    transition count from prev_tag to tag_word
    total possible transition count
    '''
    global words_to_tag_counts, tag_to_next_tag_count, tag_counts
    return (tag_to_next_tag_count[prev_tag][tag_word] + 1) / ( sum(tag_to_next_tag_count[prev_tag].values()) + len(tag_to_next_tag_count[prev_tag]) )

def calculate_transition_prob_smoothed(prev_tag):
    '''
    calculate transition probability prev_tag, tag_word
    transition count from prev_tag to tag_word
    total possible transition count
    '''
    global words_to_tag_counts, tag_to_next_tag_count, tag_counts
    return 1 / ( sum(tag_to_next_tag_count[prev_tag].values()) + len(tag_to_next_tag_count[prev_tag]) )


def join_probability(prev_tag_probability, total_prob_word_tag):
    return log10(total_prob_word_tag) + prev_tag_probability

def main_fn():
    global words_to_tag_counts, tag_to_next_tag_count, tag_counts
    # Take input dir
    test_data = sys.argv[1]
    print "Input file ", test_data
    
    with open("hmmoutput.txt", 'w') as o:
        o.close()
        
    # Read training file and count transitions and count of tag, word
    with open('hmmmodel.txt', 'r') as f:
        words_to_tag_counts = eval(f.readline())
        tag_to_next_tag_count = eval(f.readline())
        tag_counts = eval(f.readline())

        f.close();
        
    with open(test_data, 'r') as f:
        line = f.readline()
#         print line#.decode('string_escape')
        
        while line:
            '''
            dictionary with composite key (tag_word, position)
            value - prev_tag, probability  
            '''
            chain = {}
            
            words = splitLine(line.strip())
#             print words
            prev_tag_set = [START_STATE]
            position = -1
            for word in words:
                position += 1
                transition_exists = False
                
                # all the tag_to_next_tag_count for this word
                if word in words_to_tag_counts:
                    counter_tags_per_word = words_to_tag_counts[word]
                else:
                    # TODO check how to handle unknown word 
#                     print "Can't find this word in training data", position, word
                    # considering all tags as we don't know anything about this word 
                    counter_tags_per_word = Counter(tag_counts.keys())

                
                for tag_word in counter_tags_per_word:
                    
                    chain[tag_word,position] = None, NEG_INF
                                
                    # all transition from  prev_tag to tag_word
                    for prev_tag in prev_tag_set :
                        prev_tag_probability = 0
                        if (position > 0) :
                            _,prev_tag_probability = chain[prev_tag, position - 1 ]
                        
                        if tag_word in tag_to_next_tag_count[prev_tag]:
                            #TODO add smoothing
                            
                            tran_prob_prev_to_current = calculate_transition_prob( tag_word, prev_tag) 
                            # calculate emission probability word, tag_word
                            # count freq of tag | word -> counter_tags_per_word[tag_word] 
                            # count total freq of tag ->  tag_counts[tag_word]
                            em_prob_word_tag = counter_tags_per_word[tag_word] / tag_counts[tag_word]
                            
                            total_prob_word_tag = tran_prob_prev_to_current + em_prob_word_tag
                            
                            # update max probability
                            _,max_probabilty = chain[tag_word, position]
                            if join_probability(prev_tag_probability, total_prob_word_tag) > max_probabilty:
                                # value - best prev_tag, tag_word, probability
                                chain[tag_word, position] = prev_tag,join_probability(prev_tag_probability, total_prob_word_tag)
#                                 print "set ",tag_word, position , chain[tag_word, position]
                                transition_exists = True
                            
#                             print  prev_tag, tag_word, word, tag_to_next_tag_count[prev_tag][tag_word], counter_tags_per_word[tag_word] 
#                             print sum(tag_to_next_tag_count[prev_tag].values()), tran_prob_prev_to_current
#                             print tag_counts[tag_word], em_prob_word_tag
#                             print position, chain[tag_word, position]
                        else:
                            # TODO test using this block only if transition_exists = False
#                             print position,"No transition from {0} {1} ".format(prev_tag, tag_word)
                            tran_prob_prev_to_current = calculate_transition_prob_smoothed(prev_tag)
                            _,max_probabilty = chain[tag_word, position]
                            if join_probability( prev_tag_probability, tran_prob_prev_to_current) > max_probabilty:
                                chain[tag_word, position] = prev_tag, join_probability( prev_tag_probability, tran_prob_prev_to_current)
#                                 print "set ",tag_word, position , chain[tag_word, position]

                    # loop for each tag of a word ends
#                 if not transition_exists:
#                     # TODO check how to handle unknown transition
#                     print "Can't find existing transitions for {0} , prev_tag - {1} provided tags - {2}".format(word, prev_tag_set, counter_tags_per_word)
                    
                # update prev_tag
                prev_tag_set = counter_tags_per_word.keys()
                
                # loop for single word in a line ends

            # find best tag for last position
            last_word_tag = ""
            last_word_tag_probability = NEG_INF
            for tag in tag_counts:
                if (tag,len(words) - 1) in chain:
                    _,tag_prob = chain[tag, len(words) - 1]
#                     print "last_word_tag_probability", tag,len(words)
                    if(tag_prob > last_word_tag_probability):
                        last_word_tag_probability = tag_prob
                        last_word_tag = tag
            
            if not last_word_tag:
                print words   
                print chain
            # do backward chaining for words         
            tagged_words = [] + words
            for i in reversed(range(0,len(tagged_words))) :
                tag_word = tagged_words[i]+"/"+last_word_tag
                tagged_words[i] = tag_word
                last_word_tag = chain[last_word_tag,i][0]
            
#             print tagged_words
            with open("hmmoutput.txt", 'a') as o:
                for tagged_word in tagged_words:
                    o.write("{0} ".format(tagged_word))
                o.write("\n")
                o.close()

#             line = ""
            line = f.readline()
            # loop for one line ends
        print "Whole file written"
        
print __name__
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main_fn() 

