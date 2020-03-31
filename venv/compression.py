import re
import search
from nltk.stem.porter import PorterStemmer
import preprocessing

def cleanStopWords30(token):
    stop = open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/stopwords30.stop', 'r')
    stopWords = stop.read().split()
    if token!='':
        if token in stopWords:
            token = ''
        stop.close()
    return token


def cleanStopWords150(token):
    stop = open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/stopwords150.stop', 'r')
    stopWords = stop.read().split()
    if token!='':

        if token in stopWords:
            token = ''
        stop.close()
    return token

def cleannumber(token):
    if token.isnumeric():
        token=''
    return token

def case_folding(token):
    token = token.lower()
    return token

def calculate_position(diction:dict):
    pos_diction={}
    docIDindex={}
    all_raw_tokens=[]
    all_terms = diction.keys()
    all_blocks=preprocessing.block_construction()
    #merge dictionary
    for block in all_blocks:
        docIDindex.update(block)
    #get all of the raw tokens and generate a big list which contain all of the tokens
    count=[]
    #
    for term in all_terms:
       for docID in diction[term]:
          count.append(docIDindex.get(docID).count(term))
       frequency=sum(count)
       pos_diction[term]=frequency
    return pos_diction
#DF
def calculate_nonposition(diction:dict):
    nonpos_diction={}
    all_terms = diction.keys()
    for term in all_terms:
        count=len(diction[term])
        nonpos_diction[term]=count
    return nonpos_diction

def number_filter(diction:dict):
    new_diction={}
    terms=diction.keys()
    for term in terms:
        if not term.isnumeric():
            new_diction[term]=diction[term]
    return new_diction

def case_folding_filter(diction:dict):
    new_dict={}
    termfolded=""
    terms=diction.keys()
    for term in terms:
        term=case_folding(term)
        if term in new_dict:
         new_dict[term]=new_dict[term]+diction[term]
        else:
          new_dict[term]=diction[term]
    return new_dict


def stopwords30_filter(diction:dict):
    new_diction={}
    stop = open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/stopwords30.stop', 'r')
    stopWords = stop.read().split()

    terms = diction.keys()
    for term in terms:
        if term not in stopWords:
            new_diction[term]=diction[term]
    stop.close()
    return new_diction

def stopwords150_filter(diction:dict):
    new_diction = {}
    stop = open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/stopwords150.stop', 'r')
    stopWords = stop.read().split()

    terms = diction.keys()
    for term in terms:
        if term not in stopWords:
            new_diction[term] = diction[term]
    stop.close()
    return new_diction

def caluculate_sum (diction:dict):
    total=0
    for term in diction.keys():
        total=total+diction[term]
    return total






if __name__ == "__main__":
   dictionData=[]
   pos_dicData=[]
   nonpos_dicData=[]


   diction=search.readDictionary()

   pos_dic=calculate_position(diction)
   nonpos_dic=calculate_nonposition(diction)

#deal with diction
   dictionData.append(len(diction))
   dictionData.append(len(number_filter(diction)))
   # dictionData.append(len(case_folding_filter(diction)))
   dictionData.append(len(stopwords30_filter(diction)))
   dictionData.append(len(stopwords150_filter(diction)))

#deal with pos_dic
   pos_dicData.append(caluculate_sum(pos_dic))
   pos_dicData.append(caluculate_sum(number_filter(pos_dic)))
   # pos_dicData.append(caluculate_sum(case_folding_filter(pos_dic)))
   pos_dicData.append(caluculate_sum(stopwords30_filter(pos_dic)))
   pos_dicData.append(caluculate_sum(stopwords150_filter(pos_dic)))

#deal with nonpos_dic
   nonpos_dicData.append(caluculate_sum(nonpos_dic))
   nonpos_dicData.append(caluculate_sum(number_filter(nonpos_dic)))
   # nonpos_dicData.append(caluculate_sum(case_folding_filter(nonpos_dic)))
   nonpos_dicData.append(caluculate_sum(stopwords30_filter(nonpos_dic)))
   nonpos_dicData.append(caluculate_sum(stopwords150_filter(nonpos_dic)))


   print(dictionData)
   print(pos_dicData)
   print(nonpos_dicData)