import sys
import os
from nblearn import DEF_KEY, PRIOR_KEY, TRUE_KEY , FALSE_KEY, POS_KEY , NEG_KEY, tokenize_text


def get_with_def(model, token):
    if token in model:
        return model[token]
    else: 
        return model[DEF_KEY]


# Take input dir
baseDir = sys.argv[1]
print baseDir

test_files=[]
for root, dirnames, filenames in os.walk(baseDir):
    for filename in filenames:
#         if not any([x in filename.lower() for x in ["license","readme","ds_store"] ]):
        test_files.append(os.path.join(root, filename) )

#print test_files

with open('nbmodel.txt', 'r') as f:
    nbmodel = eval(''.join(f.readlines())) 
    f.close()

print "Reloaded model.." 

print "Processing records- {0}".format(len(test_files))

result = ""

for fn in test_files:
    try:
        # # All scores are logged.
        # initialize with prior for each file
        true_score = nbmodel[TRUE_KEY][PRIOR_KEY]
        false_score = nbmodel[FALSE_KEY][PRIOR_KEY]
        pos_score = nbmodel[POS_KEY][PRIOR_KEY]
        neg_score = nbmodel[NEG_KEY][PRIOR_KEY]
        #print neg_score
        with open(fn, 'r') as f:
            file_content = ' '.join(f.readlines())
                
            for test_token in tokenize_text(file_content):
                # # Add logs of individual words 
                true_score += get_with_def(nbmodel[TRUE_KEY], test_token)
                false_score += get_with_def(nbmodel[FALSE_KEY], test_token)
                pos_score += get_with_def(nbmodel[POS_KEY], test_token)
                neg_score += get_with_def(nbmodel[NEG_KEY], test_token)
                #for ends
            f.close()
        if (true_score > false_score):
            result += "truthful "
        else:
            result += "deceptive "
        if (pos_score > neg_score):
            result += "positive "
        else:
            result += "negative "
        
        result += fn + "\n"
    except:
        pass
        
#         print " --- "     
#         print file_content 
#         print true_score, false_score, pos_score, neg_score
#         print "Positive : {0}".format(pos_score > neg_score)
#         print "True : {0}".format(true_score > false_score)

    # label_a label_b path2 
    # In the above format, label_a is either truthful or deceptive, label_b is either positive or negative,
    # and pathn is the path of the text file_content being classified.
#print result

with open("nboutput.txt", 'w') as f:
    f.write(result)
    f.close()
            
print "Classification complete.."

