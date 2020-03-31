import os
import compression
import Indexing
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+[\-]?\w+')


def readDictionary():
   diction={}
   f=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/RAM/CacheDic','r')
   string=f.readline()
   while(string!=""):
    term_list=Indexing.extraction(string)
    diction[term_list[0]]=term_list[1:]
    string=f.readline()
   f.close()

   f = open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/DISK/DiskDic', 'r')
   string = f.readline()
   while (string != ""):
       term_list = Indexing.extraction(string)
       diction[term_list[0]] = term_list[1:]
       string = f.readline()
   f.close()


   return diction

def readAIDictionary():
    diction = {}
    f = open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AIRAM/CacheDic', 'r')
    string = f.readline()
    while (string != ""):
        term_list = Indexing.extraction(string)
        diction[term_list[0]] = term_list[1:]
        string = f.readline()
    f.close()

    f = open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AIDISK/DiskDic', 'r')
    string = f.readline()
    while (string != ""):
        term_list = Indexing.extraction(string)
        diction[term_list[0]] = term_list[1:]
        string = f.readline()
    f.close()


    return diction

def merge(list1:list,list2:list):
    mergedlist=[]

    mergedlist=list(set(list1+list2))


    return mergedlist


def intersection(list1:list,list2:list):
    temp=set(list1)
    intersectlist=[value for value in list2 if value in temp ]


    return intersectlist

def search_single_keyword(query,dictionay:dict):
    retrieveddocs=[]
    #split the query and clean the tokens
    querylist=query.split(" ")
    print(querylist)

    for i in range(0,len(querylist)):
        querylist[i]=compression.cleanStopWords30(querylist[i])
        querylist[i]=compression.cleanStopWords150(querylist[i])
    #search for each tokens
    for i in range(0, len(querylist)):
        if querylist[i]!='':
            for term in dictionay.keys():
                if term == querylist[i]:
                    if len(retrieveddocs)==0:
                        retrieveddocs=dictionay[term]
                    else:
                       retrieveddocs=intersection(retrieveddocs,dictionay[term])


    return retrieveddocs
#it can return empty
def AND_Search(query,dictionay:dict):
    retrieveddocs=[]
    #split the query and clean the tokens
    querylist=tokenizer.tokenize(query)

    for i in range(0,len(querylist)):
        querylist[i]=compression.cleanStopWords30(querylist[i])
        querylist[i]=compression.cleanStopWords150(querylist[i])
    #search for each tokens
    #initial the first token
    if querylist[0] in dictionay.keys():
        retrieveddocs=dictionay[querylist[0]]
    for i in range(1, len(querylist)):
        if querylist[i]!='':
            for term in dictionay.keys():
                if term == querylist[i]:
                    if len(retrieveddocs)==0:
                        return "NO RESULT"
                    else:
                       retrieveddocs=intersection(retrieveddocs,dictionay[term])

    if len(retrieveddocs)==0:
        return "NO RESULT"
    return retrieveddocs




def OR_Search(query,dictionary:dict):
    retrieveddocs = []
    # split the query and clean the tokens
    querylist = tokenizer.tokenize(query)
    for i in range(0, len(querylist)):
        querylist[i]=querylist[i].lower()

    for i in range(0, len(querylist)):
        querylist[i] = compression.cleanStopWords30(querylist[i])
        querylist[i] = compression.cleanStopWords150(querylist[i])
    # generate lower querylist:

    # search for each tokens
    for i in range(0, len(querylist)):
        if querylist[i] != '':
            for term in dictionary.keys():
                if term == querylist[i]:
                    retrieveddocs=merge(retrieveddocs,dictionary[term])

    if len(retrieveddocs) == 0:
        return "NO RESULT"
    return retrieveddocs

if __name__ == "__main__":
   diction=readDictionary()
   print(OR_Search('Artificial Intelligence',diction))