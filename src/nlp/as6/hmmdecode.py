# Tag using hmmmodel generate from hmmlearn

from collections import Counter
import sys
from hmmUtils import * 

'''
dictionary of words_to_tag_counts 
key -> word
value -> counter of tag_to_next_tag_count for this word
This will be used in emission probability
''' 
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

def main_fn():
    global words_to_tag_counts, tag_to_next_tag_count, tag_counts
    # Take input dir
    test_data = sys.argv[1]
    print "Input file ", test_data
    
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
            tokens = splitLine(line.strip())
            print tokens
            prev_tag_set = [START_STATE]
            for token in tokens:
                # all the tag_to_next_tag_count for this token
                if token in words_to_tag_counts:
                    counter_tags_per_word = words_to_tag_counts[token]
                else:
                    # TODO check how to handle unknown words_to_tag_counts 
                    continue
                
                for tag_word in counter_tags_per_word:
                    # all transition from  prev_tag to tag_word
                    for prev_tag in prev_tag_set :
                        if tag_word in tag_to_next_tag_count[prev_tag]:
                            print token, tag_word, counter_tags_per_word[tag_word] , prev_tag , tag_to_next_tag_count[prev_tag].get(tag_word)
                            #calculate transition probability prev_tag, tag_word
                            
                            # calculate emission probability token, tag_word
                            # count
                            em_prob = 1 
                    
                # update prev_tag
                prev_tag_set = counter_tags_per_word.keys()
            line = ""
    
    
print __name__
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main_fn() 

