from bs4 import BeautifulSoup
from fileinput import filename
import re
import os
import string
import nltk
from nltk.tokenize import RegexpTokenizer
# import preprocessing.py
#for one block
import preprocessing
import search
import json
tokenizer = RegexpTokenizer(r'\w+[\-]?\w+')

def SPIMI(block:dict,blocknum):
    sortedblock={}
    Invertedblock={}
    doctmentIDs=block.keys()
    for doctmentID in doctmentIDs:
        tokens=block[doctmentID]
        for token in tokens:
            token=token.lower()
            if token in Invertedblock:
                Invertedblock[token].append(doctmentID)

            else:#create a new file
                Invertedblock[token]=[]
                Invertedblock[token].append(doctmentID)



 #write the alphabetical index to the disk
    termlist=sorted(Invertedblock.keys())
    f=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/DISK/BLOCK'+str(blocknum),'w')
    for term in termlist:
      sortedblock[term]=Invertedblock[term]
      line = ( term+ ':' +' '.join(Invertedblock[term]) + '\n')
      f.write(line)

    f.close()





    return sortedblock


def SPIMIAI(block:dict,blocknum):
    sortedblock={}
    Invertedblock={}
    doctmentIDs=block.keys()
    for doctmentID in doctmentIDs:
        tokens=block[doctmentID]
        for token in tokens:
            token=token.lower()
            if token in Invertedblock:
                Invertedblock[token].append(doctmentID)

            else:#create a new file
                Invertedblock[token]=[]
                Invertedblock[token].append(doctmentID)



 #write the alphabetical index to the disk
    termlist=sorted(Invertedblock.keys())
    f=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AIDISK/BLOCK'+str(blocknum),'w')
    for term in termlist:
      sortedblock[term]=Invertedblock[term]
      line = ( term+ ':' +' '.join(Invertedblock[term]) + '\n')
      f.write(line)

    f.close()





    return sortedblock


# dic={'1234':['a','bs','cd'],'2345':['a','Edsf','adsffg'],'4675':['edsf','addd']}



#read from text and extract the term and the posting list
def extraction(line):
    term_position = line.find(':')
    term = line[0:term_position]
    term_postinglist = line[term_position + 1:].split(' ')
    term_postinglist.insert(0, term)
    return term_postinglist
# term_poslist eg: ['a','1234','4673','3333']
def find_firstword(term_list:list):
    firstword=''
    for list in term_list:
        if list!="" and (list[0] < firstword or firstword == ''):
            firstword=list[0]

    return firstword



#merge all blocks
def Mergeallblocks(numofblock):
    count=0
    memorydict=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/RAM/CacheDic','w')
    diskdic=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/DISK/DiskDic','w')
    templist=[]
    blocklist=[]
    posting=[]
   #read the files (blocks) to a list and initial a templist
    for blocknum in range(0,numofblock):
       f=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/DISK/BLOCK'+str(blocknum),'r')
       blocklist.insert(blocknum,f)
       templist.insert(blocknum,blocklist[blocknum].readline())

     # transform the string to the list
    for i in range(0, numofblock):
       templist[i] = extraction(templist[i])
    #do the merging
    while any(templist):

        #find the miniword
        miniword=find_firstword(templist)

        for i in range(0, numofblock):   #find all the  miniwords in list and replace them with nextline
          if(templist[i]!=""):
            if(templist[i][0]==miniword):
                # templist[i].remove(templist[i][0])

                posting.extend(templist[i][1:])
                templist[i].clear()
                templist[i]=(blocklist[i].readline())
                if (templist[i]!=""):
                  templist[i]=extraction(templist[i])

        #write the posting and the miniword to the dictionary

        if count<25000:
         memorydict.write(miniword+':'+' '.join(posting)+'\n')
         posting.clear()
         count+=1
        else:
          diskdic.write(miniword+':'+' '.join(posting)+'\n')
          posting.clear()



    memorydict.close()
    diskdic.close()
    f.close()

def MergeallAIblocks(numofblock):
    count=0
    memorydict=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AIRAM/CacheDic','w')
    diskdic=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AIDISK/DiskDic','w')
    templist=[]
    blocklist=[]
    posting=[]
   #read the files (blocks) to a list and initial a templist
    for blocknum in range(0,numofblock):
       f=open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AIDISK/BLOCK'+str(blocknum),'r')
       blocklist.insert(blocknum,f)
       templist.insert(blocknum,blocklist[blocknum].readline())

     # transform the string to the list
    for i in range(0, numofblock):
       templist[i] = extraction(templist[i])
    #do the merging
    while any(templist):

        #find the miniword
        miniword=find_firstword(templist)

        for i in range(0, numofblock):   #find all the  miniwords in list and replace them with nextline
          if(templist[i]!=""):
            if(templist[i][0]==miniword):
                # templist[i].remove(templist[i][0])

                posting.extend(templist[i][1:])
                templist[i].clear()
                templist[i]=(blocklist[i].readline())
                if (templist[i]!=""):
                  templist[i]=extraction(templist[i])

        #write the posting and the miniword to the dictionary

        if count<25000:
         memorydict.write(miniword+':'+' '.join(posting)+'\n')
         posting.clear()
         count+=1
        else:
          diskdic.write(miniword+':'+' '.join(posting)+'\n')
          posting.clear()



    memorydict.close()
    diskdic.close()
    f.close()
##build Index relevant with AI key words and write to file
def AIIndex():
    NUM=10000
    all_tokens=preprocessing.block_construction_AInonduplicated(NUM)
    blocknum = 0
    for block in all_tokens:
        SPIMIAI(block, blocknum)
        blocknum += 1

    MergeallAIblocks(blocknum)


    return AIIndex
    # for key in keys:
    #     if key in
if __name__ == "__main__":

    # NUM=10000
    #
    # all_tokens=preprocessing.block_construction_nonduplicated(10000)
    # blocknum=0
    # for block in all_tokens:
    #
    #     SPIMI(block,blocknum)
    #     blocknum+=1
    #
    # Mergeallblocks(blocknum)

    AI=AIIndex()
    # print(AI)