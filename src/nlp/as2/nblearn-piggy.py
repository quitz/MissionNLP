# Learn a naive bayes classification from input dir
import sys
from dircache import listdir
import string
from math import log10
from collections import Counter
from operator import itemgetter
import heapq

DEF_KEY = "__default__"
PRIOR_KEY = "__prior__"
TRUE_KEY = "true_review"
FALSE_KEY = "false_review"
POS_KEY = "pos_review"
NEG_KEY = "neg_review"

NEG = "negative_polarity"
POS = "positive_polarity"
FALSE = "/deceptive_from_MTurk"
TRUTH_NEG = "/truthful_from_Web"
TRUTH_POS = "/truthful_from_TripAdvisor"

#stop_words1_no_punc = set(["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "arent", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "cant", "cannot", "could", "couldnt", "did", "didnt", "do", "does", "doesnt", "doing", "dont", "down", "during", "each", "few", "for", "from", "further", "had", "hadnt", "has", "hasnt", "have", "havent", "having", "he", "hed", "hell", "hes", "her", "here", "heres", "hers", "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill", "im", "ive", "if", "in", "into", "is", "isnt", "it", "its", "its", "itself", "lets", "me", "more", "most", "mustnt", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shant", "she", "shed", "shell", "shes", "should", "shouldnt", "so", "some", "such", "than", "that", "thats", "the", "their", "theirs", "them", "themselves", "then", "there", "theres", "these", "they", "theyd", "theyll", "theyre", "theyve", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasnt", "we", "wed", "well", "were", "weve", "were", "werent", "what", "whats", "when", "whens", "where", "wheres", "which", "while", "who", "whos", "whom", "why", "whys", "with", "wont", "would", "wouldnt", "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself", "yourselves"])
stop_words1 = set(["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"])
stop_words2 = set(["about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "among", "an", "and", "another", "any", "anybody", "anyone", "anything", "anywhere", "are", "area", "areas", "around", "as", "ask", "asked", "asking", "asks", "at", "away", "b", "back", "backed", "backing", "backs", "be", "became", "because", "become", "becomes", "been", "before", "began", "behind", "being", "beings", "best", "better", "between", "big", "both", "but", "by", "c", "came", "can", "cannot", "case", "cases", "certain", "certainly", "clear", "clearly", "come", "could", "d", "did", "differ", "different", "differently", "do", "does", "done", "down", "down", "downed", "downing", "downs", "during", "e", "each", "early", "either", "end", "ended", "ending", "ends", "enough", "even", "evenly", "ever", "every", "everybody", "everyone", "everything", "everywhere", "f", "face", "faces", "fact", "facts", "far", "felt", "few", "find", "finds", "first", "for", "four", "from", "full", "fully", "further", "furthered", "furthering", "furthers", "g", "gave", "general", "generally", "get", "gets", "give", "given", "gives", "go", "going", "good", "goods", "got", "great", "greater", "greatest", "group", "grouped", "grouping", "groups", "h", "had", "has", "have", "having", "he", "her", "here", "herself", "high", "high", "high", "higher", "highest", "him", "himself", "his", "how", "however", "i", "if", "important", "in", "interest", "interested", "interesting", "interests", "into", "is", "it", "its", "itself", "j", "just", "k", "keep", "keeps", "kind", "knew", "know", "known", "knows", "l", "large", "largely", "last", "later", "latest", "least", "less", "let", "lets", "like", "likely", "long", "longer", "longest", "m", "made", "make", "making", "man", "many", "may", "me", "member", "members", "men", "might", "more", "most", "mostly", "mr", "mrs", "much", "must", "my", "myself", "n", "necessary", "need", "needed", "needing", "needs", "never", "new", "new", "newer", "newest", "next", "no", "nobody", "non", "noone", "not", "nothing", "now", "nowhere", "number", "numbers", "o", "of", "off", "often", "old", "older", "oldest", "on", "once", "one", "only", "open", "opened", "opening", "opens", "or", "order", "ordered", "ordering", "orders", "other", "others", "our", "out", "over", "p", "part", "parted", "parting", "parts", "per", "perhaps", "place", "places", "point", "pointed", "pointing", "points", "possible", "present", "presented", "presenting", "presents", "problem", "problems", "put", "puts", "q", "quite", "r", "rather", "really", "right", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", "second", "seconds", "see", "seem", "seemed", "seeming", "seems", "sees", "several", "shall", "she", "should", "show", "showed", "showing", "shows", "side", "sides", "since", "small", "smaller", "smallest", "so", "some", "somebody", "someone", "something", "somewhere", "state", "states", "still", "still", "such", "sure", "t", "take", "taken", "than", "that", "the", "their", "them", "then", "there", "therefore", "these", "they", "thing", "things", "think", "thinks", "this", "those", "though", "thought", "thoughts", "three", "through", "thus", "to", "today", "together", "too", "took", "toward", "turn", "turned", "turning", "turns", "two", "u", "under", "until", "up", "upon", "us", "use", "used", "uses", "v", "very", "w", "want", "wanted", "wanting", "wants", "was", "way", "ways", "we", "well", "wells", "went", "were", "what", "when", "where", "whether", "which", "while", "who", "whole", "whose", "why", "will", "with", "within", "without", "work", "worked", "working", "works", "would", "x", "y", "year", "years", "yet", "you", "young", "younger", "youngest", "your", "yours", "z"])
stop_words = stop_words1.union(stop_words2)
prior_truth = 0
prior_false = 0
prior_pos = 0
prior_neg = 0
stop_char = string.punctuation + '1234567890'
my_stop = set(['all', 'just', 'food', 'over', 'front', 'rooms', 'go', 'its', 'staff', 'finally', 'took', 'had', 'better', 'to', 'only', 'location', 'has', 'friendly', 'do', 'them', 'good', 'get', 'very', 'michigan', 'were', 'they', 'desk', 'not', 'day', 'like', 'bar', 'helpful', 'did', 'morning', 'she', 'night', 'small', 'found', 'went', 'husband', 'view', 'because', 'hard', 'some', 'back', 'bed', 'our', 'best', 'out', 'even', 'what', 'said', 'for', 'chicago', 'looking', 'everything', 'got', 'ever', 'told', 'be', 'we', 'recently', 'business', 'never', 'here', 'water', 'free', 'by', 'on', 'about', 'would', 'restaurant', 'many', 'could', 'experience', 'place', 'or', 'first', 'beautiful', 'dont', 'into', 'one', 'down', 'right', 'another', 'your', 'hotels', 'city', 'bathroom', 'from', 'service', 'area', 'there', 'two', 'been', 'next', 'their', 'much', 'too', 'way', 'recommend', 'was', 'more', 'door', 'that', 'hotel', 'great', 'but', 'downtown', 'excellent', 'an', 'with', 'than', 'he', 'me', 'made', 'room', 'this', 'up', 'us', 'will', 'while', 'can', 'of', 'didnt', 'called', 'say', 'are', 'and', 'then', 'minutes', 'is', 'am', 'it', 'comfortable', 'as', 'hilton', 'at', 'have', 'in', 'my', 'breakfast', 'check', 'if', 'again', 'nights', 'no', 'trip', 'make', 'when', 'stayed', 'any', 'also', 'other', 'which', 'you', 'really', 'nice', 'staying', 'price', 'after', 'stay', 'arrived', 'weekend', 'lobby', 'a', 'booked', 'off', 'i', 'floor', 'well', 'asked', 'beds', 'definitely', 'so', 'clean', 'time', 'the', 'staying','experience','city','chicago', 'stayed', 'trip', 'looking'])

def readAllFile(fold):
    content_arr = []
    for fn in listdir(fold):
        # print fold + fn
        with open(fold + fn, 'r') as f:
            content_arr.append(' '.join(f.readlines()))
    
    return content_arr
            
def readAllFolds(fold_dir, _fold_arr=None):
    if(_fold_arr == None):
        # TODO reserved "/fold1/" from training set for dev testing
        # _fold_arr = ["/fold2/", "/fold3/", "/fold4/"] ##dev testing
        _fold_arr = ['/' + f + '/' for f in listdir(fold_dir) if f[:1] != '.']  # dynamic, production
    # print _fold_arr 
    content_arr = []
    for fold in (fold_dir + s for s in _fold_arr):
        content_arr += readAllFile(fold)
        
    return content_arr


def tokenize_text(content):
    # # TODO implement auto-correct using phonetics
    # # TODO handle stemming include, including
    # # TODO handle line..word -> lineword
    # Removing all punctuation and number - !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    
    tokens = "".join([i for i in content if (i not in stop_char) ]).split()
    
    # Lower case everything
    tokens = [x.lower() for x in tokens]
    
    # Remove stop words
    # tokens = [x for x in tokens if x not in stop_words]
    
    return tokens

def collectAllTokens(content_array):
    result = []
    for r in content_array:
        result += tokenize_text(r)
    return result

def log_nb(num):
    return log10(num)

def calculatePText(count_occur, token_class , vocab):
    return log_nb((count_occur * 1.0) / (len(token_class) + len(vocab))) 


# stuff to run always here such as class/def
def main():
    # Take input dir
    baseDir = sys.argv[1]
    if baseDir[-1:] != '/' : baseDir += '/'
    
    print baseDir
    
    neg_review = readAllFolds(baseDir + NEG + FALSE)
    neg_review += readAllFolds(baseDir + NEG + TRUTH_NEG)
    
    pos_review = readAllFolds(baseDir + POS + FALSE)
    pos_review += readAllFolds(baseDir + POS + TRUTH_POS)
    
    false_review = readAllFolds(baseDir + NEG + FALSE)
    false_review += readAllFolds(baseDir + POS + FALSE)
    
    true_review = readAllFolds(baseDir + NEG + TRUTH_NEG)
    true_review += readAllFolds(baseDir + POS + TRUTH_POS)
    
    print "Done with reading all data.."
    print "Calculating priors.."
    prior_pos = log_nb(len(pos_review) / (len(pos_review) + len(neg_review) * 1.0))
    prior_neg = log_nb(len(neg_review) / (len(pos_review) + len(neg_review) * 1.0))
    
    prior_truth = log_nb(len(true_review) / (len(true_review) + len(false_review) * 1.0))
    prior_false = log_nb(len(false_review) / (len(true_review) + len(false_review) * 1.0))
    
    
    # list of all the tokens in each class
    true_review_token = collectAllTokens(true_review)
    false_review_token = collectAllTokens(false_review)
    pos_review_token = collectAllTokens(pos_review)
    neg_review_token = collectAllTokens(neg_review)
    
    # # Initializing counters for fast counts
    true_review_token_ctr = Counter(true_review_token)
    false_review_token_ctr = Counter(false_review_token)
    pos_review_token_ctr = Counter(pos_review_token)
    neg_review_token_ctr = Counter(neg_review_token)
        
#     my_stop = set([ite for ite, it in true_review_token_ctr.most_common(50)]) 
#     
#     my_stop = my_stop.union(set([ite for ite, it in false_review_token_ctr.most_common(50)]))
#     
#     print my_stop
#     print len(my_stop)
# 
#     print my_stop.intersection(stop_words)
#     print len(my_stop.intersection(stop_words))
# 
#     print my_stop.difference(stop_words)
#     print len(my_stop.difference(stop_words))
    least_a = set([ite+str(it) for ite, it in heapq.nsmallest(5050, true_review_token_ctr.items(), key=itemgetter(1)) ])
    least_b = set([ite+str(it) for ite, it in heapq.nsmallest(4300, false_review_token_ctr.items(), key=itemgetter(1)) ])
    print least_a
    print least_b
    print len(least_a.intersection(least_b))
    print [ite[:-1] for ite in least_a.intersection(least_b) ]
    
    all_a = set([ite+str(it) for ite, it in true_review_token_ctr.most_common() ])
    all_b = set([ite+str(it) for ite, it in false_review_token_ctr.most_common() ])

    print len(all_a.intersection(all_b))
    print [ite[:-1] for ite in all_a.intersection(all_b) ]

    print "Done with collecting all tokens.."
    # total vocab   
    vocab = set(pos_review_token + neg_review_token)
    
#     list_s = list(vocab)
#     list_s.sort()
#     print list_s
     
    training = {}
    training[TRUE_KEY] = {}
    training[FALSE_KEY] = {}
    training[POS_KEY] = {}
    training[NEG_KEY] = {}
    
    print "Calculating P(text|x) for : {0}".format(len(vocab))
    
    for word in vocab:
        # calculating counts and adding 1 as smoothing value
        count_true = 1 + true_review_token_ctr[word]
        count_false = 1 + false_review_token_ctr[word]
        count_pos = 1 + pos_review_token_ctr[word]
        count_neg = 1 + neg_review_token_ctr[word]
        
        training[TRUE_KEY][word] = calculatePText(count_true, true_review_token, vocab) 
        training[FALSE_KEY][word] = calculatePText(count_false, false_review_token, vocab) 
        training[POS_KEY][word] = calculatePText(count_pos, pos_review_token, vocab) 
        training[NEG_KEY][word] = calculatePText(count_neg, neg_review_token, vocab) 
        
    training[TRUE_KEY][DEF_KEY] = calculatePText(1, true_review_token, vocab)
    training[FALSE_KEY][DEF_KEY] = calculatePText(1, false_review_token, vocab)
    training[POS_KEY][DEF_KEY] = calculatePText(1, pos_review_token, vocab)
    training[NEG_KEY][DEF_KEY] = calculatePText(1, neg_review_token, vocab)
        
    training[TRUE_KEY][PRIOR_KEY] = prior_truth
    training[FALSE_KEY][PRIOR_KEY] = prior_false
    training[POS_KEY][PRIOR_KEY] = prior_pos
    training[NEG_KEY][PRIOR_KEY] = prior_neg
        
    print "saving results in file"
    with open('nbmodel.txt', 'w') as f:
        f.write(str(training))
        f.close()
    
    print "done"

# Checking how many times code is executed
print __name__
if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main() 
