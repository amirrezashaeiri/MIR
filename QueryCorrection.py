
from English_preprocess import *
from Persian_preprocess import *


def helpPreProcess(string, language):
    
    res = ""
    if language == "persian":
        res = string_preProcess_persian(string)   
    elif language == "english":
        res = string_preProcess_english(string)
        
    return res

 
def helpIndex(language, bigram, help):
    
    dic = None
    if language == "persian" and bigram:
        dic = help[0]  
    elif language == "english" and bigram:
        dic = help[2]
    elif language == "persian":
        dic = help[1]
    elif language == "english":
        dic = help[3]
        
    return dic


def stringCorrection(string, language, ktop=10, help):
    
    string_split = string.split()
    
    res = ""
    for x in string_split:
        
        xp = helpPreProcess(x, language)
        
        if len(xp) == 0 or len(x) == 1:
            res = res + " " + x
        else:
            xc = wordCorrection(xp[0], helpIndex(language, True, help), ktop)
            if xc == xp[0]:
                res = res + " " + x
            else:
                res = res + " " + xc
                
    res = res[1:]
    
    return res
    
    
def wordCorrection(word, dic, ktop):
    
    bigram, n_word = makeBigram(word)
    
    temp = []
    for x in bigram:
        temp += dic[x]
    words_dic = {x:temp.count(x) for x in temp}
    
    words_jacard_dic = {}
    for x, y in words_dic.items():
        _, temp_n = makeBigram(x)
        words_jacard_dic[x] = Jacard(n_word, temp_n, y)
    
    words_jacard_sorted = sorted(words_jacard_dic.items(), key=lambda item: item[1], reverse=True)
    
    words_jacard_top = words_jacard_sorted[:ktop]
    
    minimum = 1000
    correct = ""
    for x, _ in words_jacard_top:
        temp = levenshteinDistance(word, x)
        if temp < minimum:
            minimum = temp
            correct = x
    
    return correct
    
    
def makeBigram(word):
    
    bigram = []
    for i in range(len(word) - 1):
        bigram += [word[i:i + 2]]
        
    n_word = len(bigram)
    
    return bigram, n_word


def Jacard(A, B, AB):
    res = AB / (A + B - AB)
    return res
    
    
def levenshteinDistance(s1, s2):
    
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        temp_distances = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                temp_distances.append(distances[i1])
            else:
                temp_distances.append(1 + min((distances[i1], distances[i1 + 1], temp_distances[-1])))
        distances = temp_distances
    res = distances[-1]
    
    return res
  
  
