
import numpy as np

from English_preprocess import *
from Persian_preprocess import *


def helpPreProcess(string, language):
    
    res = ""
    if language == "persian":
        res = string_preProcess_persian(string)   
    elif language == "english":
        res = string_preProcess_english(string)
        
    return res

 
def helpIndex(language, bigram, indexes):
    
    dic = None
    if language == "persian" and bigram:
        dic = indexes[0]  
    elif language == "english" and bigram:
        dic = indexes[2]
    elif language == "persian":
        dic = indexes[1]
    elif language == "english":
        dic = indexes[3]
        
    return dic


def numberOfDocs(language, pre_indexes):
    
    res = ""
    if language == "persian":
        res = len(pre_indexes[0]) 
    elif language == "english":
        res = len(pre_indexes[1])
        
    return res
    

def stringSearch(string, language, indexes, pre_indexes, ktop=10):
    
    main_dic = helpIndex(language, False, indexes)
    words = list(main_dic.keys())
    n_word = len(words)
    
    n_doc = numberOfDocs(language, pre_indexes)
    
    
    vector_space_title = np.zeros((n_doc + 1, n_word))
    vector_space_text = np.zeros((n_doc + 1, n_word))

    for i, x in enumerate(main_dic, 0):
        for y in main_dic[x]['title']:
            vector_space_title[y, i] += len(main_dic[x]['title'][y])
        for y in main_dic[x]['text']:
            vector_space_text[y, i] += len(main_dic[x]['text'][y])
    
    vector_space_title = 1 + vector_space_title    
    vector_space_text = 1 + vector_space_text

    vector_space_title_idfs = np.log10((1 / np.log10(np.count_nonzero(vector_space_title, axis=0))) * n_word)
    vector_space_text_idfs = np.log10((1 / np.log10(np.count_nonzero(vector_space_text, axis=0))) * n_word)
    
    vector_space_title_tfs = np.log10(vector_space_title)
    vector_space_text_tfs = np.log10(vector_space_text)
    
    vector_space_title_tfidfs = np.multiply(vector_space_title_tfs, vector_space_title_idfs)
    vector_space_text_tfidfs = np.multiply(vector_space_text_tfs, vector_space_text_idfs)
                                       
    vector_space_title_norm = np.apply_along_axis(Normalization, 1, vector_space_title)
    vector_space_text_norm = np.apply_along_axis(Normalization, 1, vector_space_text)
    
    
    string_split = helpPreProcess(string, language)
    words_dic_tfidfs = {x:string_split.count(x) for x in string_split}
    norm = Normalization(list(words_dic_tfidfs.values()))
    words_dic_norm = {x:norm[i] for i, x in enumerate(string_split, 0)}
                                       
    
    scores = {}
    for i in range(n_doc):                      
        s = 0
        for y in words_dic_norm:
            try:
                s += words_dic_norm[y] * vector_space_title_norm[i][words.index(y)]
                s += words_dic_norm[y] * vector_space_text_norm[i][words.index(y)]
            except ValueError:
                continue

        scores[i] = s
                                       
    final = sorted(scores, key=scores.get, reverse=True)[:ktop]

    
    return final


def stringSearchProximity(string, language, indexes, pre_indexes, ktop=10, proximity=50):
                                       
    main_dic = helpIndex(language, False, indexes)
    words = list(main_dic.keys())
    n_word = len(words)
    
    n_doc = numberOfDocs(language, pre_indexes)
                                
    
    string_split = helpPreProcess(string, language)

    for x in string_split:
        try:
            temp = main_dic[x]
        except KeyError:
            return "We could not find some of your words in any document."
                                       
    
    min_index = 0
    min_lenght = 10000000
    for i in range(len(string_split)):
        temp = len(list(main_dic[string_split[i]]['text'].keys()))
        if temp < min_lenght:
            min_index = i
            min_lenght = temp

    candidate = []
    for x in main_dic[string_split[min_index]]['text']:
                                       
        main_flag = True
                                       
        for i in range(len(string_split)):
            
            if i == min_index:
                continue
            
            try:
                flag = False
                j = 0
                k = 0
                j_c = len(main_dic[string_split[min_index]]['text'][x])
                k_c = len(main_dic[string_split[i]]['text'][x])
                while j < j_c and k < k_c:
                                       
                    j_th = main_dic[string_split[min_index]]['text'][x][j]
                    k_th = main_dic[string_split[i]]['text'][x][k]
                                       
                    if abs(j_th - k_th) <= proximity:
                        flag = True
                        break
                    elif j_th - k_th < - proximity:
                        j += 1           
                    else:
                        k += 1
                                       
                if not flag:
                    main_flag = False
                    break

            except KeyError:
                main_flag = False
                break
         
        if main_flag:
              candidate += [x]
                                       
                                       
    sorted_docs = stringSearch(string, language, indexes, pre_indexes, ktop=10000000)
    
    final = []
    for x in sorted_docs:
        try:
            temp = candidate.index(x)
            final += [x]
        except ValueError:
            continue
    
                                       
    final = final[:ktop]
    return final
                                       
                                       
def Normalization(x):
    res = x / np.linalg.norm(x, ord=2)
    return res
                                       
                                       
