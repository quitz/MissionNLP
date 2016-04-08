# Utility function to help in counting parsing etc..

START_STATE = "Q0"

def splitWordAndTag(token):
    '''
    I/P - token - word/tag
    O/P - wrod, tag
    '''
    indexOfSlash = token.rfind("/")
    return token[:indexOfSlash], token[indexOfSlash+1:]


def splitLine(line):
    '''
    I/P - line from input file
    O/P - list of tokens delimeted by space
    '''
    return line.split(" ")


# print splitWordAndTag("//FF")