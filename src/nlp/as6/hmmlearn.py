# Train a hmmmodel using training data

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
    training_file = sys.argv[1]
    print "Input file ", training_file
    
    # Read training file and count transitions and count of tag, word
    with open(training_file, 'r') as f:
        line = f.readline()
#         print line#.decode('string_escape')
        
        while line:
            tokens = splitLine(line.strip())
        
            prev_tag = START_STATE
            for token in tokens:
                word,tag = splitWordAndTag(token)
                #update count of tag
                tag_counts.update([tag])
                
                #store emission counts
                if word not in words_to_tag_counts: 
                    words_to_tag_counts[word]=Counter()
                    
                words_to_tag_counts[word].update([tag])   
                
                #store transition counts
                if(prev_tag):
                    if prev_tag not in tag_to_next_tag_count: 
                        tag_to_next_tag_count[prev_tag]=Counter()
                        
                    tag_to_next_tag_count[prev_tag].update([tag])
                    
                prev_tag = tag
                
            line = f.readline()
#             line = ""
            # while close 
        f.close()
        # with closed
        
    # Calculate emission and transition probability from counts in hmmdecode.py
    print "saving results in file"
    
    with open('hmmmodel.txt', 'w') as f:
        f.write(str(words_to_tag_counts))
        f.write("\n")
        f.write(str(tag_to_next_tag_count))
        f.write("\n")
        f.write(str(tag_counts))
        f.write("\n")
        f.close()
    
    print "done"
    
    
#     print str(words_to_tag_counts).decode('string_escape')
#     print ""
#     print str(tag_to_next_tag_count).decode('string_escape')
#     print ""
#     print str(tag_counts)

print __name__
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main_fn() 
