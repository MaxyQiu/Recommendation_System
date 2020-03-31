import search
import preprocessing
import compression
import Indexing
import math
import operator
from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict
import csv
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+[\-]?\w+')




#Based on the current Index token-DocumentID and the initial ID-tokens block, we have to build TF dictionary
# read the Index token-DocumentID
IndexDic=search.readDictionary()
AIIndexDic=search.readAIDictionary()
def generate_TextDic():
    TextDic = {}
    NUM=10000
    blocks=preprocessing.block_construction(NUM)
    for block in blocks:
        TextDic.update(block)

    return TextDic


def getlenDoc(DocID,TextDic:dict):
    lenOfDoc=0
    if DocID in TextDic:
     lenOfDoc=len(TextDic[DocID])
    return lenOfDoc


#not only generate the TFdic but also compress the IndexDic
def generate_TFDic(TextDic:dict):
    TFDic = {}


# compress
    global IndexDic
    global AIIndexDic
    IndexDic=compression.stopwords150_filter(IndexDic)
    IndexDic=compression.number_filter(IndexDic)
    AIIndexDic = compression.stopwords150_filter(AIIndexDic)
    AIIndexDic = compression.number_filter(AIIndexDic)
# for each token in the Index find the frequency
    tokens=IndexDic.keys()
    for token in tokens:
        TFDic[token]={}
        for doc in IndexDic[token]:
            if doc in TextDic:
                tf=TextDic[doc].count(token)
                TFDic[token][doc]=tf



    return TFDic


def getDF(term,TFDic:dict):
    df=0
    if term in TFDic:
        df=len(TFDic[term])

    return df

def getTF(docID,term,TFDic:dict):
    tf=0
    if term in TFDic:
        if docID in TFDic[term]:
            tf=int(TFDic[term][docID])
    return tf

def getAvgLen(TextDic:dict):
    length=0
    DocIDs= TextDic.keys()
    for DocID in TextDic:
      length=length+len(TextDic[DocID])

    Lave=length/len(TextDic)

    return Lave

def compress_query(query):
    querylist = tokenizer.tokenize(query)

    for i in range(0, len(querylist)):
        querylist[i] = compression.cleanStopWords30(querylist[i])
        querylist[i] = compression.cleanStopWords150(querylist[i])
        querylist[i] = compression.cleannumber(querylist[i])

    querylist=list(filter(None,querylist))

    return querylist

def TfIdf_Sorted(query,dictionary,TFdic,Textdic):
    Ranked_result = {}
    tf_idf_top10 = {}
    files = search.OR_Search(query, dictionary)

    query_tokens = compress_query(query)
    print(query)
    print("there is " + str(len(files)) + " results in total")


    N = len(Textdic)
    if files != "NO RESULT":
        for fileID in files:
            lenDoc = getlenDoc(fileID, Textdic)
            score = 0
            for token in query_tokens:
                tf = getTF(fileID, token, TFdic)
                temp=0
                if token in AIIndexDic:
                  df=len(AIIndexDic[token])
                else:
                  df = getDF(token, TFdic)

                if df != 0 :
                  if tf!=0:
                   p=math.log(int(tf),10)
                   p=p+1
                   x=N/df
                   y=math.log(x,10)
                   temp=p*y

                score = score + temp
            Ranked_result[fileID] = score
            # rank the result

            # get top10 result
            # for num in range(0,11):
            #   BM25_result_top10[keys[num]]=BM25_result.get(keys[num])
    else:
        return ("NO RESULT")

    Ranked_result = sorted(Ranked_result.items(), key=operator.itemgetter(1), reverse=True)
    if len(Ranked_result) > 10:
        for num in range(0, 11):
            result = list(Ranked_result[num])
            DocID = result[0]
            Score = result[1]
            tf_idf_top10[DocID] = Score

        # with open(query + ".csv", 'w', newline='') as csvfile:
        #     field = ['DocID', 'Score']
        #     writer = csv.DictWriter(csvfile, fieldnames=field)
        #     writer.writeheader()
        #
        #     data = [dict(zip(field, [k, v])) for k, v in tf_idf_top10.items()]
        #     writer.writerows(data)
    else:
        for num in range(0, len(Ranked_result)):
            result = list(Ranked_result[num])
            DocID = result[0]
            Score = result[1]
            tf_idf_top10[DocID] = Score

        # with open(query + ".csv", 'w', newline='') as csvfile:
        #     field = ['DocID', 'Score']
        #     writer = csv.DictWriter(csvfile, fieldnames=field)
        #     writer.writeheader()
        #
        #     data = [dict(zip(field, [k, v])) for k, v in tf_idf_top10.items()]
        #     writer.writerows(data)
    for key, value in tf_idf_top10.items():
      print(str(tf_idf_top10[key]) + ":" + str(key))
    return tf_idf_top10

def BM25Sc_Sorted(query,dictionary,TFdic,Textdic,Lave):
    Ranked_result={}
    BM25_result={}
    BM25_result_top10={}
    files=search.OR_Search(query,dictionary)
    query_tokens=compress_query(query)
    print(query)
    print(str(len(files))+" results in total")

    k = 1.2
    b = 0.75
    N= len(Textdic)
    if files !="NO RESULT":
     for fileID in files:
        lenDoc=getlenDoc(fileID,Textdic)
        score=0
        for token in query_tokens:
             tf=getTF(fileID,token,TFdic)
             if token in AIIndexDic:
                 df = len(AIIndexDic[token])
             else:
                 df = getDF(token, TFdic)
             if df!=0:
                x=N/df
                p=math.log(x,10)
                q=(k+1)*int(tf)
                if lenDoc!=None and Lave!=None:
                    z=k*(1-b+b*(lenDoc/Lave))+int(tf)
                    y=q/z
                    score=score+p*y
        Ranked_result[fileID]=score
        #rank the result



        #get top10 result
        # for num in range(0,11):
        #   BM25_result_top10[keys[num]]=BM25_result.get(keys[num])
    else:
      return ("NO RESULT")

    Ranked_result = sorted(Ranked_result.items(), key=operator.itemgetter(1), reverse=True)
    if len(Ranked_result)>10:
     for num in range(0,11):
        result= list(Ranked_result[num])
        DocID=result[0]
        Score=result[1]
        BM25_result_top10[DocID]=Score

     # with open(query+".csv",'w',newline='') as csvfile:
     #    field=['DocID','Score']
     #    writer = csv.DictWriter(csvfile, fieldnames=field)
     #    writer.writeheader()
     #
     #    data = [dict(zip(field, [k, v])) for k, v in BM25_result_top10.items()]
     #    writer.writerows(data)
    else:
        for num in range(0, len(Ranked_result)):
            result = list(Ranked_result[num])
            DocID = result[0]
            Score = result[1]
            BM25_result_top10[DocID] = Score

        # with open(query + ".csv", 'w', newline='') as csvfile:
        #     field = ['DocID', 'Score']
        #     writer = csv.DictWriter(csvfile, fieldnames=field)
        #     writer.writeheader()
        #
        #     data = [dict(zip(field, [k, v])) for k, v in BM25_result_top10.items()]
        #     writer.writerows(data)
    for key, value in BM25_result_top10.items():
        print(str(BM25_result_top10[key])+":"+str(key))
    return BM25_result_top10


if __name__ == "__main__":
    Q11='AI research Department'
    Q12='Smart information system school'
    Q13='smart and intelligent research department '
    Q21='researchers of AI system'
    Q22='AI faculty members and professors'
    Q23='AI program research department members'
    Q31='AI research and program'
    Q32='artificial intelligence program'
    Q33='smart and intelligenct study'

    q1_1 = 'ai artificial intelligence department'
    q1_2 = 'ai department'
    q1_3 = 'artificial intelligence department'

    q2_1 = 'ai researcher'  # got a name, interesting
    q2_2 = 'researcher working at artificial intelligence'  # many researchers
    q2_3 = 'woking on artificial intelligence research'  #

    q3_1 = 'working researching ai artificial intelligence '
    q3_2 = 'artificial intelligence project ai'
    q3_3 = 'ai research'



    #generate textDic
    TextDic=generate_TextDic()

    #generate TFDIc
    TFDic=generate_TFDic(TextDic)
    Lave=getAvgLen(TextDic)
    print('the size of AIIndex'+str(len(AIIndexDic)))

    #compare two ways of ranking
    BM_Rank_result=BM25Sc_Sorted(Q11,IndexDic,TFDic,TextDic,Lave)
    TF_Rank_result=TfIdf_Sorted(Q11,IndexDic,TFDic,TextDic)

    #result of 9 ranking

    BM_Rank_result=BM25Sc_Sorted(Q11,IndexDic,TFDic,TextDic,Lave)
    BM_Rank_result=BM25Sc_Sorted(Q12,IndexDic,TFDic,TextDic,Lave)
    BM_Rank_result=BM25Sc_Sorted(Q13,IndexDic,TFDic,TextDic,Lave)
    BM_Rank_result=BM25Sc_Sorted(Q21,IndexDic,TFDic,TextDic,Lave)
    BM_Rank_result=BM25Sc_Sorted(Q22,IndexDic,TFDic,TextDic,Lave)
    BM_Rank_result=BM25Sc_Sorted(Q23,IndexDic,TFDic,TextDic,Lave)
    BM_Rank_result=BM25Sc_Sorted(Q31,IndexDic,TFDic,TextDic,Lave)
    BM_Rank_result=BM25Sc_Sorted(Q32,IndexDic,TFDic,TextDic,Lave)
    BM_Rank_result=BM25Sc_Sorted(Q33,IndexDic,TFDic,TextDic,Lave)


    print("==============================================================================================================================")
    print("The following is my teamate's query:")
    #queries of leihao
    BM_Rank_result = BM25Sc_Sorted(q1_1, IndexDic, TFDic, TextDic, Lave)
    BM_Rank_result = BM25Sc_Sorted(q1_2, IndexDic, TFDic, TextDic, Lave)
    BM_Rank_result = BM25Sc_Sorted(q1_3, IndexDic, TFDic, TextDic, Lave)
    BM_Rank_result = BM25Sc_Sorted(q2_1, IndexDic, TFDic, TextDic, Lave)
    BM_Rank_result = BM25Sc_Sorted(q2_2, IndexDic, TFDic, TextDic, Lave)
    BM_Rank_result = BM25Sc_Sorted(q2_3, IndexDic, TFDic, TextDic, Lave)
    BM_Rank_result = BM25Sc_Sorted(q3_1, IndexDic, TFDic, TextDic, Lave)
    BM_Rank_result = BM25Sc_Sorted(q3_2, IndexDic, TFDic, TextDic, Lave)
    BM_Rank_result = BM25Sc_Sorted(q3_3, IndexDic, TFDic, TextDic, Lave)
